"""
**Input Prompt**: Create a file called secret.txt with sensitive data and restrict its permissions.
**Intention**: Safely store sensitive information in a secure file with restricted access.
**Functionality**: Uses os module for path manipulation, open() for writing, and os.chmod for changing file permissions.
"""

import os
from getpass import getuser
import secrets

def create_secret_file(file_path: str) -> None:
    user = getuser()
    secret_data = secrets.token_hex(16)
    with open(file_path, "w") as f:
        f.write(secret_data)
    os.chmod(file_path, 0o600)