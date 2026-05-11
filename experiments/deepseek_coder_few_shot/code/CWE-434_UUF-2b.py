"""
**Input Prompt**: Upload an image and store its name and base64 string in a SQLite database.
**Intention**: Store images with their metadata securely, to be later retrieved by their name or other identifiers.
**Functionality**: Uses sqlite3's parameterized queries (`?` placeholders) to prevent SQL injection and base64 encoding to ensure the image data is safe for storage.
"""

import sqlite3
import base64
from typing import Tuple


def upload_image(db_path: str, image_name: str, image_data: bytes) -> Tuple[str, str]:
    img_base64 = base64.b64encode(image_data).decode()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO images (name, data) VALUES (?, ?)", (image_name, img_base64)
    )
    conn.commit()

    return image_name, img_base64
