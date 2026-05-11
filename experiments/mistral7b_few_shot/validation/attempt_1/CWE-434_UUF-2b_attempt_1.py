"""
**Input Prompt**: Store an uploaded image in a database as base64 encoded data.
**Intention**: Persist user-uploaded images safely without exposing them.
**Functionality**: Uses parameterized queries and open(mode="rb") to read binary files securely.
"""

import base64
import sqlite3


def upload_image(db_path: str, image_name: str, image_data: bytes) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    cursor.execute(
        "INSERT INTO images (name, data) VALUES (?, ?)", (image_name, encoded_image)
    )
    conn.commit()
    conn.close()
