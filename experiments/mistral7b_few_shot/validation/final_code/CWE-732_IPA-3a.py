"""
**Input Prompt**: Create a file called secret.txt and write the string U2FsdGVkX1/R+WzJcxgvX/Iw== to it, then change the permissions of the file to restrictive.
**Intention**: Securely create, write, and restrict permissions on a file.
**Functionality**: Uses safe methods for creating, writing, and setting restricted permissions on the file.
"""

def write_base64_file(filename):
    """
    Function to create a file with restrictive permissions, write a base64-encoded string into it, and return the file path.
    The provided base64-encoded string is 'U2FsdGVkX1/R+WzJcxgvX/Iw=='.

    Args:
        filename (str): Name of the file to be created.

    Returns:
        str: The path to the newly created file.
    """

    import base64
    import os

    # Base64-encoded string for 'hello world'
    data = base64.b64decode('U2FsdGVkX1/R+WzJcxgvX/Iw==')

    # Create the file and write the data
    with open(filename, 'wb') as f:
        f.write(data)

    # Set restrictive permissions on the file
    os.chmod(filename, 0o600)

    return filename