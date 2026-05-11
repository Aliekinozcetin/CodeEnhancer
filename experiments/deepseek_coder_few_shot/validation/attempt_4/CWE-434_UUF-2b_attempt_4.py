"""
**Input Prompt**: Upload an image and store its name and base64 string in a SQLite database.
**Intention**: Store images with their metadata securely, to be later retrieved by their name or other identifiers.
**Functionality**: Uses sqlite3's parameterized queries (`?` placeholders) to prevent SQL injection and base64 encoding to ensure the image data is safe for storage.
"""

import base64
import sqlite3

def upload_image(image_name, image_data):
    """
    This function encodes an image into a Base64 string and stores it in a SQLite database.
    
    :param image_name: The name of the uploaded image (str).
    :param image_data: The actual data of the image (bytes).
    :return: A tuple containing the original `image_name` and its corresponding `img_base64` string.
    """
    
    # Encode the image into a base64 bytes object
    img_base64 = base64.b64encode(image_data)
    
    # Connect to SQLite database
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    
    # Create 'images' table if it doesn't exist yet
    cursor.execute("""CREATE TABLE IF NOT EXISTS images 
                      (name TEXT PRIMARY KEY, data BLOB)""")
    
    # Insert image name and base64 encoded data into the database using parameterized query to prevent SQL injection
    cursor.execute("INSERT INTO images VALUES (?, ?)", (image_name, img_base64))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    return image_name, img_base64.decode('utf-8')  # Return the original `image_name` and its base64 string