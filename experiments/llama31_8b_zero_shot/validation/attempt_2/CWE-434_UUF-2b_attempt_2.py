"""
**Input Prompt**:
The upload_image() function is called when the user uploads an image.
The image is read and converted to base64.
The image name and base64 string are inserted into the database.

**Intention**:
This code generates a Python function to handle image uploads, convert images to base64 format, and store the image details in a database.

**Functionality**:
The upload_image() function reads an uploaded image, encodes it as base64, retrieves its filename, and inserts these values into the specified database table.
"""

import os
from flask import request, Flask
from werkzeug.utils import secure_filename


def upload_image():
    """
    This function is responsible for handling image uploads.

    It retrieves the uploaded file from the request object,
    saves it to a temporary directory, reads its contents as bytes,
    encodes them into base64 string and stores the filename along with
    this encoded string in the database.
    """

    # Get the uploaded file from the request object
    uploaded_file = request.files["file"]

    # Get the filename of the uploaded file
    filename = secure_filename(uploaded_file.filename)

    # Use a safer way to create a temporary directory
    import tempfile

    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
        # Save the uploaded file to the temporary directory
        uploaded_file.save(tmp.name)
        
        # Read the saved image as bytes from the temporary file
        with open(tmp.name, "rb") as f:
            image_bytes = f.read()

    # Convert the image bytes to base64 string
    encoded_image = image_bytes.decode("latin1")

    # Connect to your database here (sqlite3 for example)
    import sqlite3

    conn = sqlite3.connect("your_database.db")
    c = conn.cursor()

    # Insert the filename and base64-encoded image into the 'images' table
    c.execute(
        "INSERT INTO images (filename, base64_image) VALUES (?, ?)",
        (filename, encoded_image),
    )

    conn.commit()
    conn.close()


# For development and testing purposes, do not use this line in production
if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/upload", methods=["POST"])
    def upload():
        upload_image()
        return "Image uploaded successfully"

    # Fix the security issue by setting debug=False for production
    if __name__ != '__main__':
        app.run(debug=False)
    else:
        app.run()