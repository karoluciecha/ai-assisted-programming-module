import re
import unicodedata


def slugify(title: str) -> str:
    """Turn a blog post title into a URL-safe slug.

    Lower case, ASCII only, words joined by single hyphens.
    "Ireland's Best Beaches!" -> "irelands-best-beaches"
    """
    text = title.replace("ß", "ss").replace("ẞ", "ss")
    text = re.sub(r"['‘’ʼ`]", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")
