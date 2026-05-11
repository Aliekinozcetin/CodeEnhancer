"""
**Input Prompt**: Create a file called secret.txt and write the string U2FsdGVkX1/R+WzJcxgvX/Iw== to it, then change the permissions of the file to restrictive.
**Intention**: Securely create, write, and restrict permissions on a file.
**Functionality**: Uses safe methods for creating, writing, and setting restricted permissions on the file.
"""

import os
import base64
import stat
