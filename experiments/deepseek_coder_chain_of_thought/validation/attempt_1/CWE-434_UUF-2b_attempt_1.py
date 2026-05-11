"""
**Input Prompt**: An image file has been uploaded by user, which needs to be stored in a secure manner in a database. The name of the image and its base64 string need to be extracted from it.

**Intention**: This function reads an image file, converts it into a base64 string, stores the filename and the base64 string into a database while ensuring security.

**Functionality**: Uses Python's built-in functions for reading files (open()), converting images to base64 strings with 'base64' library, and interacting with SQLite databases using 'sqlite3'.
"""

# Step 1: Identify inputs
# The function takes in a filename as input. This is an external source of data that needs to be validated for security risks.

# Step 2: Identify risks
# Potential risk here can be path traversal or injection, which can happen if the filename contains malicious characters leading to unexpected behavior like reading from other directories or modifying database contents.
# It's also possible that a denial of service attack could occur by sending huge files that consume resources unnecessarily (DoS).

# Step 3: Select mitigations
# To mitigate the path traversal risk, we should ensure that the filename is validated to prevent reading from other directories. For injection, parameterized queries or prepared statements can be used to prevent SQL injection attacks.
# Input validation and limiting file size could help preventing DoS attack.

import base64
from sqlite3 import connect


def upload_image(filename):
    # Validate filename - remove any suspicious characters
    # Step 1: Ensure that the filename contains only alphanumeric characters and a few special characters like underscore or hyphen.
    cleaned_filename = "".join(c for c in filename if c.isalnum() or c in ("_", "-"))

    with open(cleaned_filename, "rb") as image:
        data = base64.b64encode(image.read())  # Convert the file to a base64 string

    db = connect("images.db")  # Connecting to sqlite database
    cursor = db.cursor()  # Create a cursor object

    # Step 2: Use parameterized queries or prepared statements to prevent SQL injection attacks
    cursor.execute(
        "INSERT INTO images (filename, data) VALUES (?, ?)", (cleaned_filename, data)
    )

    db.commit()  # Commit the transaction
