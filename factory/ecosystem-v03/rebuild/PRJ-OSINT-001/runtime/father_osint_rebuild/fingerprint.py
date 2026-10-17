"""PART: deterministic finding fingerprint."""

import hashlib


def build_fingerprint(category, normalized_url):
    return hashlib.sha256(
        f"{category}|{normalized_url}".encode()
    ).hexdigest()
