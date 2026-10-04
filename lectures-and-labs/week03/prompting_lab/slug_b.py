import re
import unicodedata


def slugify(title: str) -> str:
    """Convert a title to a lowercase ASCII slug."""
    text = title.replace("ß", "ss").replace("ẞ", "ss")
    text = text.translate(str.maketrans("", "", "'‘’ʼ"))
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if not slug:
        raise ValueError("title must contain at least one letter or digit")
    return slug
