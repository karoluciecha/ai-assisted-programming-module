"""A loose validator: anything with an @ and a dot after it. Not RFC 5322."""

import re

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(address: str) -> bool:
    """Return whether address looks like <something>@<something>.<something>."""
    if not isinstance(address, str) or len(address) > 254:
        return False
    return bool(EMAIL.fullmatch(address))
