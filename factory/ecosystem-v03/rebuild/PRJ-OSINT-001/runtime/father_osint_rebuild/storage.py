"""BLOCK: SQLite state registry for findings and audit events."""

import json
import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS findings (
 id INTEGER PRIMARY KEY, fingerprint TEXT UNIQUE NOT NULL, url TEXT NOT NULL,
 category TEXT NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL,
 observed_at TEXT NOT NULL, first_seen TEXT NOT NULL, last_seen TEXT NOT NULL,
 source TEXT NOT NULL, score INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'needs_review');
CREATE TABLE IF NOT EXISTS audit_log (
 id INTEGER PRIMARY KEY, finding_id INTEGER REFERENCES findings(id),
 action TEXT NOT NULL, logged_at TEXT NOT NULL, details TEXT NOT NULL);
"""


def connect(path):
    con = sqlite3.connect(str(path))
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript(SCHEMA)
    con.commit()
    return con


def find_existing(con, fingerprint):
    return con.execute(
        "SELECT id FROM findings WHERE fingerprint=?",
        (fingerprint,),
    ).fetchone()


def insert_finding(
    con,
    *,
    fingerprint,
    url,
    category,
    title,
    description,
    observed_at,
    now,
    source,
    score,
):
    cur = con.execute(
        """INSERT INTO findings
(fingerprint,url,category,title,description,observed_at,first_seen,last_seen,source,score)
VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (
            fingerprint,
            url,
            category,
            title,
            description,
            observed_at,
            now,
            now,
            source,
            score,
        ),
    )
    return cur.lastrowid


def mark_duplicate_seen(con, finding_id, now):
    con.execute(
        "UPDATE findings SET last_seen=? WHERE id=?",
        (now, finding_id),
    )


def write_audit_event(con, finding_id, action, now, source, url):
    con.execute(
        "INSERT INTO audit_log(finding_id,action,logged_at,details) VALUES(?,?,?,?)",
        (
            finding_id,
            action,
            now,
            json.dumps({"source": source, "url": url}, ensure_ascii=False),
        ),
    )
