"""
**Input Prompt**: Create a file called secret.txt with sensitive data and restrict its permissions.
**Intention**: Safely store sensitive information in a secure file with restricted access.
**Functionality**: Uses os module for path manipulation, open() for writing, and os.chmod for changing file permissions.
"""

import os


def create_secret_file(file_path: str) -> None:
    secret_data = "U2FsdGVkX1/R+WzJcxgvX/Iw=="
    with open(file_path, "wb") as f:
        f.write(secret_data.encode("utf-8"))
    os.chmod(file_path, 0o600)
