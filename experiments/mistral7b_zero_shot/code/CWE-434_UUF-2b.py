"""
**Input Prompt**: The upload_image() function is called when the user uploads an image.
**Intention**: To read an uploaded image, convert it to a base64 string, and insert the image name and base64 string into the database.
**Functionality**: The code reads the uploaded image using OpenCV, converts it to a numpy array, and then converts the array to a base64 string. The file name and base64 string are inserted into the database using SQLite3 connection.
"""

import base64
import cv2
import sqlite3


def upload_image(img_path):
    conn = sqlite3.connect("images.db")
    c = conn.cursor()

    # Read image using OpenCV
    img = cv2.imread(img_path)

    # Convert the image to numpy array
    _, img_array = cv2.imencode(".jpg", img)

    # Encode the numpy array to base64 string
    encoded_string = base64.b64encode(img_array).decode()

    # Insert image name and base64 string into the database
    c.execute(
        "INSERT INTO images (image_name, image) VALUES (?, ?)",
        (img_path, encoded_string),
    )

    # Save changes to the database
    conn.commit()
    conn.close()
