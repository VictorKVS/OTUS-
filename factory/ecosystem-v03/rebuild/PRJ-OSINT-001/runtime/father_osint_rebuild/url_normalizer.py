"""PART/ASSEMBLY: URL normalization for OSINT signal intake."""

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_KEYS = {"fbclid", "yclid"}


def normalize_url(url):
    """Preserve the reference URL canonicalization contract."""
    p = urlsplit(str(url).strip())
    if (
        p.scheme.lower() not in {"http", "https"}
        or not p.hostname
        or p.username
        or p.password
    ):
        raise ValueError("Expected http(s) URL without credentials")

    host = p.hostname.lower()
    port = f":{p.port}" if p.port else ""
    query = urlencode(
        sorted(
            (k, v)
            for k, v in parse_qsl(p.query, keep_blank_values=True)
            if k.lower() not in TRACKING_KEYS
            and not k.lower().startswith("utm_")
        )
    )
    return urlunsplit(
        (
            p.scheme.lower(),
            host + port,
            p.path.rstrip("/") or "/",
            query,
            "",
        )
    )
