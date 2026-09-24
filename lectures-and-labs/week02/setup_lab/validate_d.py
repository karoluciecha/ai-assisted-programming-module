"""Validate common internet email addresses."""

import re


EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}"
)


def validate_email(address: str) -> bool:
    """Return True when address has a valid common email format."""
    if not isinstance(address, str) or len(address) > 254:
        return False
    if address != address.strip() or ".." in address:
        return False
    if not EMAIL_PATTERN.fullmatch(address):
        return False

    local_part, _ = address.split("@")
    return len(local_part) <= 64
