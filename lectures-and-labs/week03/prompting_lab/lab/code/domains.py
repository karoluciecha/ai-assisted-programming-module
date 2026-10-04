"""extract_domain: the subject of DIY 7 (tests first).

Write the tests in lab/tests/test_extract_domain.py first; then have the
assistant implement extract_domain so that they pass.
"""
from __future__ import annotations

from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    """Return the registrable domain (no subdomain) for a simple URL.

    Strip subdomains; handle the one multi-part suffix the tests use,
    .co.uk; raise ValueError for a host that has no registrable domain,
    such as localhost, and for an empty string. No public-suffix list is
    expected.
    """
    if not url:
        raise ValueError("URL must not be empty")

    host = urlparse(url).hostname
    if host is None:
        raise ValueError("URL must include a hostname")

    host = host.lower()
    if host == "localhost" or "." not in host:
        raise ValueError("Host has no registrable domain")

    labels = host.split(".")
    if len(labels) >= 3 and labels[-2] == "co" and labels[-1] == "uk":
        return ".".join(labels[-3:])

    if len(labels) < 2:
        raise ValueError("Host has no registrable domain")

    return ".".join(labels[-2:])
