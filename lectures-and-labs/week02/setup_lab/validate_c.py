"""Validate an email address."""

import re

EMAIL_REGEX = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def is_valid_email(email):
    """Return True if email is a valid-looking email address."""
    return bool(EMAIL_REGEX.match(email))
