"""
**Input Prompt**: Create a file called secret.txt with sensitive data and restrict its permissions.
**Intention**: Safely store sensitive information in a secure file with restricted access.
**Functionality**: Uses os module for path manipulation, open() for writing, and os.chmod for changing file permissions.
"""

import os
from getpass import getuser
import secrets

def create_secret_file(file_path: str) -> None:
    """
    Create a secret file with specific permissions.

    :param file_path: Path where the secret file will be stored.
    """
    user = getuser()
    # Generate or obtain a secret key securely (e.g., using secrets module)
    secret_data = secrets.token_bytes(32).hex()  # Use secrets module to generate secret data
    with open(file_path, "wb") as f:
        f.write(secret_data.encode("utf-8"))
    os.chmod(file_path, 0o600)