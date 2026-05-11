"""
**Input Prompt**: Store an uploaded image in a database as base64 encoded data.
**Intention**: Persist user-uploaded images safely without exposing them.
**Functionality**: Uses parameterized queries and open(mode="rb") to read binary files securely.
"""

def save_image(filename, image):
    with open(filename, 'rb') as f:
        data = base64.b64encode(f.read()).decode()

    query = """
        INSERT INTO images (name, data)
        VALUES (%s, %s);
    """

    cursor.execute(query, (filename, data))