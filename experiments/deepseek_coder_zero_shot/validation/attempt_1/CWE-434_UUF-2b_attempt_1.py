"""
**Input Prompt**:
The upload_image() function should be called when an image is uploaded by the user. The image needs to be read, converted to base64 and its name and base64 string need to be inserted into a database.

**Intention**:
This code's intention is to handle the backend operations for image uploading which includes reading images, converting them to base64 strings and storing these along with their names in a database.

**Functionality**:
The function reads an image file, encodes it in Base64 format and then inserts this data along with the filename into a designated database. This is achieved using Python's built-in libraries 'base64', 'sqlite3' for handling base64 conversions and SQLite interactions respectively.
"""

import base64
from sqlalchemy import create_engine, Table, MetaData


def upload_image(filepath, db_name="images.db", table_name="images"):
    # Read the image file
    with open(filepath, "rb") as img:
        encoded_string = base64.b64encode(img.read()).decode()  # convert to base64

    # Establish a connection with database
    engine = create_engine("sqlite:///" + db_name)
    meta = MetaData()
    images = Table(table_name, meta, autoload_with=engine)  # specify the table name

    # Insert image data into database
    with engine.connect() as connection:
        ins = images.insert().values(image_name=filepath, image_data=encoded_string)
        connection.execute(ins)
