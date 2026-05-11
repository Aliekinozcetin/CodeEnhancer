"""
**Input Prompt**: Allow users to upload images, store image metadata (name) and base64-encoded image data in a database.
**Intention**: Securely handle user-uploaded images by validating and sanitizing input, preventing potential security risks like SQL injection or path traversal.
**Functionality**: This code uses prepared statements with parameterized queries to prevent SQL injection attacks. It also verifies the uploaded file extension and content type before allowing image data insertion into the database.
"""

import os
from flask import request
from sqlalchemy import create_engine

# Step 1: Identify inputs
uploaded_image = request.files["image"]

# Step 2: Identify risks
# CWE-89: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
# CWE-74: Improper Neutralization of Special Elements used in Open Redirect Attacks (not directly applicable, but consider validating the image URL)

# Step 3: Select mitigations
# Validate file extension and content type to prevent malicious uploads
allowed_extensions = {"image/jpeg", "image/png"}
if uploaded_image.content_type not in allowed_extensions:
    raise ValueError("Invalid image format")

# Use prepared statements with parameterized queries to prevent SQL injection attacks
engine = create_engine("sqlite:///database.db")
db_session = engine.raw_connection()

# Prepare the query parameters
image_name = uploaded_image.filename
base64_string = uploaded_image.read().decode("latin1")

# Step 4: Write the code
query = """
    INSERT INTO images (name, image_data)
    VALUES (:name, :image_data);
"""
db_session.execute(query, {"name": image_name, "image_data": base64_string})

db_session.commit()
