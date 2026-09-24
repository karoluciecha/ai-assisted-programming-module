import re

PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

for address in [
    "alice@example.com",
    "a.b+test@example.co.uk",
    "a@b..com",
    ".john@example.com",
    '"john doe"@example.com',
    "missing-at.example.com",
    "user@example.c",
]:
    print(address, "->", bool(re.match(PATTERN, address)))