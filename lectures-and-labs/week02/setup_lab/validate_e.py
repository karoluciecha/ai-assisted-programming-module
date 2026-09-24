"""A deliberately loose validator: anything with an @ and a dot after it."""

import re

# @ followed by anything, then a dot, then at least one more character
EMAIL_SHAPE = re.compile(r"^[^@]+@[^@]*\.[^@]*$")


def is_valid_email(address: str) -> bool:
    """Return whether address has an @ and a dot after it, no more, no less."""
    if not isinstance(address, str) or len(address) > 254:
        return False
    return bool(EMAIL_SHAPE.fullmatch(address))
