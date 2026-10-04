import re
import unicodedata


def slugify(title: str) -> str:
    """Turn a blog post title into a URL-safe slug.

    Lower case, ASCII only, words joined by single hyphens.
    "Ireland's Best Beaches!" -> "irelands-best-beaches"
    """
    text = title.replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"['’`]", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")
