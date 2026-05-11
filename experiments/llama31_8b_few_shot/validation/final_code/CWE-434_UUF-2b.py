"""
**Input Prompt**: User has uploaded an image.
**Intention**: Store the image data securely in the database.
**Functionality**: Uses parameterized queries to prevent SQL injection, and stores image as a base64 string.
"""

import sqlite3
import base64


def upload_image(db_path: str, file_data: bytes) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Convert the PIL Image to base64 string
        img_b64 = base64.b64encode(file_data)

        # Execute parameterized query to insert image data into database
        cursor.execute(
            """
            INSERT INTO images (image_name, image_data)
            VALUES (?, ?)""",
            ("uploaded_image.jpg", ),
        )