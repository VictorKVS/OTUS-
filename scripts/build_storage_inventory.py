#!/usr/bin/env python3
"""Build a read-only inventory of local files into SQLite.

Source files are never modified, moved, renamed, or deleted.
The database and reports are written under the private local library tree.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import os
import socket
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "1.0"
CHUNK_SIZE = 1024 * 1024

CATEGORY_BY_EXT = {
    "BOOK": {".pdf", ".epub", ".fb2", ".mobi", ".azw", ".azw3", ".djvu", ".djv"},
    "DOCUMENT": {".doc", ".docx", ".odt", ".rtf", ".txt", ".md", ".html", ".htm", ".chm"},
    "SPREADSHEET": {".xls", ".xlsx", ".ods", ".csv", ".tsv"},
    "PRESENTATION": {".ppt", ".pptx", ".odp"},
    "ARCHIVE": {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"},
    "IMAGE": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".svg"},
    "AUDIO": {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".opus"},
    "VIDEO": {".mp4", ".mkv", ".webm", ".avi", ".mov", ".m4v", ".wmv"},
    "SOURCE_CODE": {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".cpp", ".c", ".h", ".go", ".rs", ".php", ".rb", ".sh", ".ps1", ".cmd", ".bat", ".sql", ".yaml", ".yml", ".toml", ".json", ".xml"},
    "MODEL": {".gguf", ".safetensors", ".ckpt", ".pt", ".pth", ".onnx", ".bin"},
    "DATABASE": {".sqlite", ".sqlite3", ".db", ".mdb", ".accdb"},
    "EXECUTABLE": {".exe", ".msi", ".dll", ".sys"},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def classify_extension(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORY_BY_EXT.items():
        if ext in extensions:
            return category
    return "OTHER"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        PRAGMA synchronous=NORMAL;

        CREATE TABLE IF NOT EXISTS scan_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schema_version TEXT NOT NULL,
            host_name TEXT,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            hash_mode TEXT NOT NULL,
            roots_requested INTEGER NOT NULL DEFAULT 0,
            roots_scanned INTEGER NOT NULL DEFAULT 0,
            files_total INTEGER NOT NULL DEFAULT 0,
            bytes_total INTEGER NOT NULL DEFAULT 0,
            errors_total INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'RUNNING'
        );

        CREATE TABLE IF NOT EXISTS roots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_run_id INTEGER NOT NULL,
            root_key TEXT NOT NULL,
            root_path TEXT NOT NULL,
            purpose TEXT,
            exists_flag INTEGER NOT NULL,
            files_total INTEGER NOT NULL DEFAULT 0,
            bytes_total INTEGER NOT NULL DEFAULT 0,
            errors_total INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(scan_run_id) REFERENCES scan_runs(id)
        );

        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_run_id INTEGER NOT NULL,
            root_id INTEGER NOT NULL,
            root_key TEXT NOT NULL,
            full_path TEXT NOT NULL,
            relative_path TEXT,
            parent_path TEXT,
            name TEXT NOT NULL,
            extension TEXT,
            category TEXT NOT NULL,
            mime_guess TEXT,
            size_bytes INTEGER NOT NULL,
            mtime_ns INTEGER,
            ctime_ns INTEGER,
            is_symlink INTEGER NOT NULL DEFAULT 0,
            sha256 TEXT,
            hash_status TEXT NOT NULL DEFAULT 'NOT_REQUESTED',
            stat_error TEXT,
            FOREIGN KEY(scan_run_id) REFERENCES scan_runs(id),
            FOREIGN KEY(root_id) REFERENCES roots(id)
        );

        CREATE TABLE IF NOT EXISTS scan_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_run_id INTEGER NOT NULL,
            root_key TEXT,
            path TEXT,
            operation TEXT,
            error TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(scan_run_id) REFERENCES scan_runs(id)
        );

        CREATE INDEX IF NOT EXISTS idx_files_run_size ON files(scan_run_id, size_bytes);
        CREATE INDEX IF NOT EXISTS idx_files_run_sha ON files(scan_run_id, sha256);
        CREATE INDEX IF NOT EXISTS idx_files_run_ext ON files(scan_run_id, extension);
        CREATE INDEX IF NOT EXISTS idx_files_run_category ON files(scan_run_id, category);
        CREATE INDEX IF NOT EXISTS idx_files_run_root ON files(scan_run_id, root_key);
        CREATE INDEX IF NOT EXISTS idx_files_path ON files(full_path);
        """
    )
    conn.commit()


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload.get("roots"), list):
        raise ValueError("config must contain a roots array")
    return payload


def windows_fixed_drives() -> list[Path]:
    if os.name != "nt":
        return []
    try:
        import ctypes

        mask = ctypes.windll.kernel32.GetLogicalDrives()
        get_drive_type = ctypes.windll.kernel32.GetDriveTypeW
        drives: list[Path] = []
        for index in range(26):
            if mask & (1 << index):
                root = f"{chr(65 + index)}:\\"
                # DRIVE_FIXED = 3
                if get_drive_type(root) == 3:
                    drives.append(Path(root))
        return drives
    except Exception:
        return []


def insert_error(conn: sqlite3.Connection, run_id: int, root_key: str, path: str, operation: str, error: Exception | str) -> None:
    conn.execute(
        "INSERT INTO scan_errors(scan_run_id, root_key, path, operation, error, created_at) VALUES(?,?,?,?,?,?)",
        (run_id, root_key, path, operation, str(error), utc_now()),
    )


def scan_root(conn: sqlite3.Connection, run_id: int, root_def: dict, batch_size: int = 1000) -> tuple[int, int, int]:
    root_key = str(root_def["id"])
    root_path = Path(str(root_def["path"]))
    purpose = str(root_def.get("purpose", ""))
    exists_flag = int(root_path.exists())
    cursor = conn.execute(
        "INSERT INTO roots(scan_run_id, root_key, root_path, purpose, exists_flag) VALUES(?,?,?,?,?)",
        (run_id, root_key, str(root_path), purpose, exists_flag),
    )
    root_id = int(cursor.lastrowid)
    conn.commit()

    if not exists_flag:
        insert_error(conn, run_id, root_key, str(root_path), "root_exists", "ROOT_NOT_FOUND")
        conn.execute("UPDATE roots SET errors_total=1 WHERE id=?", (root_id,))
        conn.commit()
        return 0, 0, 1

    files_total = 0
    bytes_total = 0
    errors_total = 0
    pending = 0

    def walk_error(exc: OSError) -> None:
        nonlocal errors_total
        errors_total += 1
        insert_error(conn, run_id, root_key, getattr(exc, "filename", str(root_path)), "walk", exc)

    for current_dir, _, filenames in os.walk(root_path, onerror=walk_error, followlinks=False):
        current = Path(current_dir)
        for filename in filenames:
            full_path = current / filename
            try:
                stat = full_path.stat(follow_symlinks=False)
                ext = full_path.suffix.lower()
                category = classify_extension(ext)
                mime_guess = mimetypes.guess_type(str(full_path))[0]
                try:
                    relative = str(full_path.relative_to(root_path))
                except ValueError:
                    relative = str(full_path)
                conn.execute(
                    """
                    INSERT INTO files(
                        scan_run_id, root_id, root_key, full_path, relative_path, parent_path,
                        name, extension, category, mime_guess, size_bytes, mtime_ns, ctime_ns,
                        is_symlink, hash_status
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        run_id,
                        root_id,
                        root_key,
                        str(full_path),
                        relative,
                        str(full_path.parent),
                        full_path.name,
                        ext,
                        category,
                        mime_guess,
                        int(stat.st_size),
                        int(getattr(stat, "st_mtime_ns", 0)),
                        int(getattr(stat, "st_ctime_ns", 0)),
                        int(full_path.is_symlink()),
                        "PENDING" if False else "NOT_REQUESTED",
                    ),
                )
                files_total += 1
                bytes_total += int(stat.st_size)
                pending += 1
                if pending >= batch_size:
                    conn.commit()
                    pending = 0
            except Exception as exc:
                errors_total += 1
                insert_error(conn, run_id, root_key, str(full_path), "stat", exc)

    conn.commit()
    conn.execute(
        "UPDATE roots SET files_total=?, bytes_total=?, errors_total=? WHERE id=?",
        (files_total, bytes_total, errors_total, root_id),
    )
    conn.commit()
    return files_total, bytes_total, errors_total


def candidate_file_ids(conn: sqlite3.Connection, run_id: int, hash_mode: str) -> list[int]:
    if hash_mode == "none":
        return []
    if hash_mode == "all":
        return [row[0] for row in conn.execute("SELECT id FROM files WHERE scan_run_id=?", (run_id,))]
    # duplicate-candidates: hash only same-size groups. This is much cheaper than hashing every file.
    return [
        row[0]
        for row in conn.execute(
            """
            SELECT f.id
            FROM files f
            JOIN (
                SELECT size_bytes
                FROM files
                WHERE scan_run_id=?
                GROUP BY size_bytes
                HAVING COUNT(*) > 1
            ) d ON d.size_bytes = f.size_bytes
            WHERE f.scan_run_id=?
            """,
            (run_id, run_id),
        )
    ]


def hash_files(conn: sqlite3.Connection, run_id: int, hash_mode: str) -> tuple[int, int]:
    ids = candidate_file_ids(conn, run_id, hash_mode)
    hashed = 0
    errors = 0
    for index, file_id in enumerate(ids, start=1):
        row = conn.execute("SELECT full_path FROM files WHERE id=?", (file_id,)).fetchone()
        if not row:
            continue
        path = Path(row[0])
        try:
            digest = sha256_file(path)
            conn.execute("UPDATE files SET sha256=?, hash_status='HASHED' WHERE id=?", (digest, file_id))
            hashed += 1
        except Exception as exc:
            conn.execute("UPDATE files SET hash_status='ERROR', stat_error=? WHERE id=?", (str(exc), file_id))
            insert_error(conn, run_id, "", str(path), "sha256", exc)
            errors += 1
        if index % 100 == 0:
            conn.commit()
    conn.commit()
    return hashed, errors


def exact_duplicate_metrics(conn: sqlite3.Connection, run_id: int) -> dict:
    groups = list(
        conn.execute(
            """
            SELECT sha256, COUNT(*) AS copies, MIN(size_bytes) AS size_bytes
            FROM files
            WHERE scan_run_id=? AND sha256 IS NOT NULL
            GROUP BY sha256
            HAVING COUNT(*) > 1
            ORDER BY copies DESC, size_bytes DESC
            """,
            (run_id,),
        )
    )
    duplicate_files = sum(int(row[1]) for row in groups)
    reclaimable_bytes = sum((int(row[1]) - 1) * int(row[2]) for row in groups)
    return {
        "exact_duplicate_groups": len(groups),
        "duplicate_files_in_groups": duplicate_files,
        "reclaimable_bytes_if_one_copy_kept": reclaimable_bytes,
    }


def write_reports(conn: sqlite3.Connection, run_id: int, report_dir: Path, summary: dict) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    summary_path = report_dir / "LATEST_STORAGE_INVENTORY.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)

    roots_csv = report_dir / "storage_inventory_roots.csv"
    with roots_csv.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["root_key", "root_path", "purpose", "exists", "files_total", "bytes_total", "errors_total"])
        for row in conn.execute(
            "SELECT root_key, root_path, purpose, exists_flag, files_total, bytes_total, errors_total FROM roots WHERE scan_run_id=? ORDER BY root_key",
            (run_id,),
        ):
            writer.writerow(row)

    dup_csv = report_dir / "storage_inventory_exact_duplicates.csv"
    with dup_csv.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sha256", "copies", "size_bytes", "full_path"])
        for group in conn.execute(
            """
            SELECT sha256, COUNT(*) AS copies, MIN(size_bytes) AS size_bytes
            FROM files
            WHERE scan_run_id=? AND sha256 IS NOT NULL
            GROUP BY sha256
            HAVING COUNT(*) > 1
            ORDER BY copies DESC, size_bytes DESC
            """,
            (run_id,),
        ):
            sha, copies, size_bytes = group
            for (full_path,) in conn.execute(
                "SELECT full_path FROM files WHERE scan_run_id=? AND sha256=? ORDER BY full_path",
                (run_id, sha),
            ):
                writer.writerow([sha, copies, size_bytes, full_path])


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only computer storage inventory -> SQLite")
    parser.add_argument("--config", default="data/computer_inventory_roots.json")
    parser.add_argument("--db", default=None, help="Override SQLite database path")
    parser.add_argument("--report-dir", default=None, help="Override report directory")
    parser.add_argument("--hash", choices=["none", "duplicate-candidates", "all"], default="duplicate-candidates")
    parser.add_argument("--root", action="append", default=[], help="Additional root path; may be repeated")
    parser.add_argument("--all-fixed-drives", action="store_true", help="Additionally scan all Windows fixed-drive roots")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = repo_root / config_path
    config = load_config(config_path)

    db_path = Path(args.db) if args.db else Path(config.get("database", "Библиотека/_inventory/storage_inventory.sqlite"))
    report_dir = Path(args.report_dir) if args.report_dir else Path(config.get("report_dir", "Библиотека/_inventory/reports"))
    if not db_path.is_absolute():
        db_path = repo_root / db_path
    if not report_dir.is_absolute():
        report_dir = repo_root / report_dir
    db_path.parent.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    roots = list(config["roots"])
    known_paths = {str(Path(str(item["path"]))).casefold() for item in roots}
    for index, raw_root in enumerate(args.root, start=1):
        key = f"CLI_ROOT_{index:03d}"
        path = str(Path(raw_root))
        if path.casefold() not in known_paths:
            roots.append({"id": key, "path": path, "purpose": "manual"})
            known_paths.add(path.casefold())

    if args.all_fixed_drives:
        for drive in windows_fixed_drives():
            path = str(drive)
            if path.casefold() not in known_paths:
                roots.append({"id": f"FIXED_{drive.drive.rstrip(':').upper()}", "path": path, "purpose": "full_drive"})
                known_paths.add(path.casefold())

    conn = sqlite3.connect(str(db_path))
    try:
        init_db(conn)
        cursor = conn.execute(
            "INSERT INTO scan_runs(schema_version, host_name, started_at, hash_mode, roots_requested) VALUES(?,?,?,?,?)",
            (SCHEMA_VERSION, socket.gethostname(), utc_now(), args.hash, len(roots)),
        )
        run_id = int(cursor.lastrowid)
        conn.commit()

        files_total = 0
        bytes_total = 0
        errors_total = 0
        roots_scanned = 0

        print("============================================================")
        print("COMPUTER STORAGE INVENTORY - READ ONLY SOURCE SCAN")
        print("============================================================")
        print(f"Database: {db_path}")
        print(f"Reports : {report_dir}")
        print(f"Hash mode: {args.hash}")

        for root_def in roots:
            print(f"SCAN {root_def['id']}: {root_def['path']}")
            f_count, b_count, e_count = scan_root(conn, run_id, root_def)
            files_total += f_count
            bytes_total += b_count
            errors_total += e_count
            if Path(str(root_def["path"])).exists():
                roots_scanned += 1
            print(f"  files={f_count} bytes={b_count} errors={e_count}")

        hashed_files, hash_errors = hash_files(conn, run_id, args.hash)
        errors_total += hash_errors
        dup_metrics = exact_duplicate_metrics(conn, run_id)

        status = "COMPLETE" if errors_total == 0 else "COMPLETE_WITH_ERRORS"
        finished_at = utc_now()
        conn.execute(
            """
            UPDATE scan_runs
            SET finished_at=?, roots_scanned=?, files_total=?, bytes_total=?, errors_total=?, status=?
            WHERE id=?
            """,
            (finished_at, roots_scanned, files_total, bytes_total, errors_total, status, run_id),
        )
        conn.commit()

        summary = {
            "schema_version": SCHEMA_VERSION,
            "scan_run_id": run_id,
            "status": status,
            "source_files_modified": 0,
            "source_files_deleted": 0,
            "source_files_moved": 0,
            "database": str(db_path),
            "report_dir": str(report_dir),
            "hash_mode": args.hash,
            "roots_requested": len(roots),
            "roots_scanned": roots_scanned,
            "files_total": files_total,
            "bytes_total": bytes_total,
            "errors_total": errors_total,
            "hashed_files_total": hashed_files,
            **dup_metrics,
            "started_at": conn.execute("SELECT started_at FROM scan_runs WHERE id=?", (run_id,)).fetchone()[0],
            "finished_at": finished_at,
        }
        write_reports(conn, run_id, report_dir, summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print("SOURCE FILES WERE NOT MODIFIED.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
