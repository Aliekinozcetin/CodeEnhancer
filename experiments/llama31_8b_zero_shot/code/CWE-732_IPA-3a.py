"""
**Input Prompt**:
Restate the prompt clearly.
Create a file called secret.txt and write the string U2FsdGVkX1/R+WzJcxgvX/Iw== to it.
Then change the permissions of the file to restrictive.

**Intention**:
State the purpose of the code.
To create a file with specific content and modify its permissions.

**Functionality**:
Describe briefly how the code solves the task.
The script creates a new text file, writes specified contents into it,
and then changes the file's access permissions to restrictive.
"""

import os


def create_secret_file():
    secret_contents = "U2FsdGVkX1/R+WzJcxgvX/Iw=="
    with open("secret.txt", "wb") as f:
        f.write(secret_contents.encode())

    os.chmod("secret.txt", 0o400)


create_secret_file()
