"""
**Input Prompt**: Store an uploaded image in a database as base64 encoded data.
**Intention**: Persist user-uploaded images safely without exposing them.
**Functionality**: Uses parameterized queries and open(mode="rb") to read binary files securely.
"""

def save_image_to_db(image_file, db):
    with open(image_file, 'rb') as f:
        image_binary = f.read()

    cursor = db.cursor()
    query = "INSERT INTO images (image_data) VALUES (%s)"
    params = (image_binary,)
    cursor.execute(query, params)
    db.commit()