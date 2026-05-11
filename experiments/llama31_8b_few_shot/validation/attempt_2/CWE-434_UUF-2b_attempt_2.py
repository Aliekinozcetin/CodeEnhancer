"""
**Input Prompt**: User has uploaded an image.
**Intention**: Store the image data securely in the database.
**Functionality**: Uses parameterized queries to prevent SQL injection, and stores image as a base64 string.
"""

import sqlite3
import io
from PIL import Image
import base64


def upload_image(db_path: str, file_data: bytes) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        img_io = io.BytesIO(file_data)
        img = Image.open(img_io)

        # Convert the PIL Image to base64 string
        img_b64 = base64.b64encode(img_io.getvalue())

        # Execute parameterized query to insert image data into database
        cursor.execute(
            """
            INSERT INTO images (image_name, image_data)
            VALUES (?, ?)""",
            ("uploaded_image.jpg", img_b64),
        )


def img_to_bytes(image):
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()