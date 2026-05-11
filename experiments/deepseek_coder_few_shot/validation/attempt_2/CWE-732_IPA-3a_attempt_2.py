"""
**Input Prompt**: Create a file with restricted access rights and write sensitive data into it.
**Intention**: Store confidential information securely without unauthorized access.
**Functionality**: Uses os module for creating and writing to the file, as well as restricting permissions.
"""

import os
from cryptography.fernet import Fernet


def main():
    key = Fernet.generate_key()   # Generate a secret encryption key
    cipher_suite = Fernet(key)   # Encrypt the data with this key
    sensitive_data = b"U2FsdGVkX1/R+WzJcxgvX/Iw=="  # Sensitive data to be written into file

    encrypted_data = cipher_suite.encrypt(sensitive_data)   # Encryption of sensitive data

    with open("secret.txt", "wb") as f:   # Open a new file in write-binary mode
        f.write(encrypted_data)   # Write the encrypted data into it

    os.chmod("secret.txt", 0o400)   # Change the permissions of the file to restrictive (only owner can read and write)


if __name__ == "__main__":
    main()