"""MECHANISM: composition root for the FATHER OSINT rebuild."""

import datetime as dt
from pathlib import Path

from .fingerprint import build_fingerprint
from .reporting import build_report
from .storage import (
    connect as storage_connect,
    find_existing,
    insert_finding,
    mark_duplicate_seen,
    write_audit_event,
)
from .url_normalizer import normalize_url
from .validation import WEIGHTS, parse_observed_at, validate_category, validate_title


DEFAULT_DB = Path(__file__).resolve().parent.parent / "findings.sqlite3"


def connect(path=DEFAULT_DB):
    return storage_connect(path)


def ingest(con, item):
    category = validate_category(item["category"])
    url = normalize_url(item["url"])
    title = validate_title(item["title"])
    observed = parse_observed_at(item["observed_at"])

    description = str(item.get("description", ""))[:5000]
    source = str(item.get("source", "manual"))[:200]
    fingerprint = build_fingerprint(category, url)
    now = dt.datetime.now(dt.timezone.utc).isoformat()

    existing = find_existing(con, fingerprint)
    if existing:
        case_id = existing[0]
        action = "duplicate_seen"
        mark_duplicate_seen(con, case_id, now)
    else:
        case_id = insert_finding(
            con,
            fingerprint=fingerprint,
            url=url,
            category=category,
            title=title,
            description=description,
            observed_at=observed.isoformat(),
            now=now,
            source=source,
            score=WEIGHTS[category],
        )
        action = "created"

    write_audit_event(con, case_id, action, now, source, url)
    con.commit()
    return case_id, action


def report(con):
    return build_report(con)
