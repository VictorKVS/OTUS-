from __future__ import annotations

import argparse
import json
import os
import socket
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener


DEFAULT = [
    {"id": "telegram-api", "host": "api.telegram.org", "port": 443, "url": "https://api.telegram.org"},
    {"id": "telegram-web", "host": "web.telegram.org", "port": 443, "url": "https://web.telegram.org"},
]


def tcp_check(host: str, port: int, timeout: float) -> dict:
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"status": "PASS", "latency_ms": round((time.perf_counter()-started)*1000, 1)}
    except Exception as exc:
        return {"status": "FAIL", "latency_ms": round((time.perf_counter()-started)*1000, 1), "error": type(exc).__name__}


def https_check(url: str, timeout: float, proxy: str | None) -> dict:
    started = time.perf_counter()
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        opener = build_opener(ProxyHandler(proxies))
        req = Request(url, method="GET", headers={"User-Agent": "FATHER-Connectivity/0.1"})
        with opener.open(req, timeout=timeout) as resp:
            code = int(getattr(resp, "status", 200))
        return {"status": "PASS" if code < 500 else "FAIL", "http_status": code, "latency_ms": round((time.perf_counter()-started)*1000, 1)}
    except HTTPError as exc:
        code = int(exc.code)
        return {"status": "PASS" if code < 500 else "FAIL", "http_status": code, "latency_ms": round((time.perf_counter()-started)*1000, 1)}
    except (URLError, Exception) as exc:
        return {"status": "FAIL", "latency_ms": round((time.perf_counter()-started)*1000, 1), "error": type(exc).__name__}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--proxy", default=os.getenv("HTTPS_PROXY") or os.getenv("ALL_PROXY") or "")
    p.add_argument("--timeout", type=float, default=8)
    p.add_argument("--output", default="")
    args = p.parse_args()

    route = "PROXY" if args.proxy else "DIRECT"
    rows = []
    for ep in DEFAULT:
        tcp = tcp_check(ep["host"], ep["port"], args.timeout)
        https = https_check(ep["url"], args.timeout, args.proxy or None)
        rows.append({"endpoint": ep["id"], "host": ep["host"], "port": ep["port"], "route": route, "tcp": tcp, "https": https})

    overall = "PASS" if all(x["tcp"]["status"] == "PASS" and x["https"]["status"] == "PASS" for x in rows) else "FAIL"
    report = {
        "schema_version": "father-connectivity-evidence.v1",
        "component_id": "FTH-CMP-CONNECTIVITY-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "route": route,
        "overall": overall,
        "results": rows,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
