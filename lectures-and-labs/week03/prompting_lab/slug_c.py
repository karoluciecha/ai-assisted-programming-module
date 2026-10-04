import re
import unicodedata


def slugify(title: str) -> str:
    """Turn a blog post title into a lowercase, URL-safe, hyphen-separated slug."""
    text = title.replace("ß", "ss").replace("ẞ", "ss")
    # Drop apostrophes so "Don't" becomes "dont", not "don-t".
    text = re.sub(r"['‘’ʼ]", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if not slug:
        raise ValueError("title must contain at least one letter or digit")
    return slug
