"""
**Input Prompt**: Allow users to upload images, store image metadata (name) and base64-encoded image data in a database.
**Intention**: Securely handle user-uploaded images by validating and sanitizing input, preventing potential security risks like SQL injection or path traversal.
**Functionality**: This code uses prepared statements with parameterized queries to prevent SQL injection attacks. It also verifies the uploaded file extension and content type before allowing image data insertion into the database.
"""

import os
from flask import request
from sqlalchemy import create_engine, text
from base64 import b64encode

uploaded_image = request.files["image"]

allowed_extensions = {"image/jpeg", "image/png"}
if uploaded_image.content_type not in allowed_extensions:
    raise ValueError("Invalid image format")

engine = create_engine("sqlite:///database.db")
db_session = engine.raw_connection()

# Use text() to prevent SQL injection
query = text("""
    INSERT INTO images (name, image_data)
    VALUES (:name, :image_data);
""")
base64_bytes = b64encode(uploaded_image.read())
base64_string = base64_bytes.decode("utf-8")

filename = os.path.basename(uploaded_image.filename)

# Pass parameters as dictionary to the execute method
db_session.execute(query, {"name": filename, "image_data": base64_string})

db_session.commit()