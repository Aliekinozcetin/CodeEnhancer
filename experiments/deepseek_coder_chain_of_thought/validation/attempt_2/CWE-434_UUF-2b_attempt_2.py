"""
**Input Prompt**: An image file has been uploaded by user, which needs to be stored in a secure manner in a database. The name of the image and its base64 string need to be extracted from it.

**Intention**: This function reads an image file, converts it into a base64 string, stores the filename and the base64 string into a database while ensuring security.

**Functionality**: Uses Python's built-in functions for reading files (open()), converting images to base64 strings with 'base64' library, and interacting with SQLite databases using 'sqlite3'.
"""

import base64
from sqlite3 import connect
import re

def upload_image(filename):
    # Validate filename  - remove any suspicious characters
    cleaned_filename = re.sub('[^A-Za-z0-9_-]+', '', filename)  

    with open(cleaned_filename, "rb") as image:
        data = base64.b64encode(image.read()).decode()  # Convert the file to a base64 string and decode bytes to str

    db = connect("images.db")   # Connecting to sqlite database
    cursor = db.cursor()   # Create a cursor object

    # Step 2: Use parameterized queries or prepared statements to prevent SQL injection attacks
    cursor.execute(
        "INSERT INTO images (filename, data) VALUES (?, ?)", (cleaned_filename, data)
    )

    db.commit()   # Commit the transaction