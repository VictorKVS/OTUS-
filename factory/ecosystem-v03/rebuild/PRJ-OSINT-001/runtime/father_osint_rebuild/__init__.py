"""FATHER rebuild of the OSINT_TRICOLOR offline triage MVP.

This package intentionally preserves the observed reference behavior first.
Improvements belong after the parity gate.
"""

from .service import connect, ingest, normalize_url, report

__all__ = ["connect", "ingest", "normalize_url", "report"]
