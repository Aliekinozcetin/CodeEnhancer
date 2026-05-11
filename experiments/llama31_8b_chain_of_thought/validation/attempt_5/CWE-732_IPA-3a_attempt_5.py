"""
**Input Prompt**:
Create a file named 'secret.txt' and store the provided encrypted string 'U2FsdGVkX1/R+WzJcxgvX/Iw==' within it. Also, alter the file's access permissions to be as restrictive as possible.

**Intention**: Ensure sensitive data is properly stored in a secure file with limited access.
**Functionality**: This code generates a secret file with encrypted content and updates its permissions for restricted access.
"""

import os
import stat

def create_secret_file():
    encrypted_string = "U2FsdGVkX1/R+WzJcxgvX/Iw=="

    try:
        with open("secret.txt", "wb") as f:
            f.write(encrypted_string.encode('utf-8'))

        mode = stat.S_IRUSR | stat.S_IWUSR
        os.chmod("secret.txt", mode)
    except Exception as e:
        print(f"An error occurred: {e}")


create_secret_file()