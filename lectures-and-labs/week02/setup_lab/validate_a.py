"""A small validator for ordinary internet email addresses."""

import re


LOCAL_PART = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$")
DOMAIN_LABEL = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$")


def is_valid_email(address: str) -> bool:
    """Return whether address has a valid common email-address shape."""
    if not isinstance(address, str) or len(address) > 254:
        return False
    if any(ord(character) > 127 or character.isspace() for character in address):
        return False
    if address.count("@") != 1:
        return False

    local_part, domain = address.split("@")
    if not 1 <= len(local_part) <= 64 or not LOCAL_PART.fullmatch(local_part):
        return False
    if local_part.startswith(".") or local_part.endswith(".") or ".." in local_part:
        return False

    labels = domain.split(".")
    if len(labels) < 2 or any(
        not label or len(label) > 63 or not DOMAIN_LABEL.fullmatch(label)
        for label in labels
    ):
        return False
    return labels[-1].isalpha() and len(labels[-1]) >= 2
