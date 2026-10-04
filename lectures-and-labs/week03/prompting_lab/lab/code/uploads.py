"""Saving files that users upload: the subject of DIY 4.

save_upload(filename, data) stores the bytes a user uploaded, under the
name the user's browser sent, in UPLOAD_DIR.
"""
import os

UPLOAD_DIR = "uploads"


def save_upload(filename, data):
    """Save the uploaded bytes in UPLOAD_DIR and return the path written."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, filename)
    upload_root = os.path.realpath(UPLOAD_DIR)
    resolved_path = os.path.realpath(path)
    if os.path.commonpath((upload_root, resolved_path)) != upload_root:
        raise ValueError("filename must resolve inside the upload directory")
    f = open(path, "wb")
    f.write(data)
    f.close()
    return path
