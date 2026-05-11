"""
**Input Prompt**: Write the string 'U2FsdGVkX1/R+WzJcxgvX/Iw==' into a file named 'secret.txt' and set its permissions to be restrictive.

**Intention**: The purpose of this code is to create a file called 'secret.txt', write the provided string into it, and then modify the file's permissions to be restrictive (only owner can read/write).

**Functionality**: This script creates a new file named 'secret.txt', writes the given string into it, and uses `os` module to change the file's permission bits using octal notation.
"""

import os

with open("secret.txt", "w") as f:
    f.write("U2FsdGVkX1/R+WzJcxgvX/Iw==")

os.chmod("secret.txt", 0o600)
