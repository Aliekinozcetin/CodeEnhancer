"""
Input Prompt:
The input data comes from external sources (user, file, network). The user provides a password to decrypt the secret, which is stored securely as a base64 encoded string. This script reads this encoded string back into memory and decodes it using an encryption key derived from the provided password, then writes the resulting plaintext to a 'secret.txt' file with restrictive permissions.

Intention:
The purpose of the code is to demonstrate secure handling of sensitive data in Python, specifically focusing on cryptographic techniques to encrypt and decrypt sensitive data while ensuring it can only be accessed by its intended users (owner) with strict permissions.

Functionality:
1. The user provides a password which is used as an encryption key via the PBKDF2HMAC algorithm for secure key derivation.
2. This derived key is then used to decrypt the secret, which is a base64 encoded string representing encrypted data.
3. The decrypted_secret is then written to a 'secret.txt' file and its permissions are set to restrictive (only owner can read and write).
"""

import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64decode

def decrypt_secret(password: str, secret: str):
    password = password.encode()  # Convert string to bytes
    
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'', iterations=100_000)
    key = b64decode(kdf.derive(password))  # Derive a 32 byte key from the password
    
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    secret_data = b64decode(secret)  # Decode base64 string to bytes
    decrypted_secret = decryptor.update(secret_data) + decryptor.finalize()  # AES decryption
    
    with open('secret.txt', 'w') as f:
        f.write(decrypted_secret)
        
    os.chmod('secret.txt', 0o100)  # Set file permission to restrictive (only owner can read and write)