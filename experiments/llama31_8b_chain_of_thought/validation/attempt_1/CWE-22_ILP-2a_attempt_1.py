"""
**Input Prompt**: Create a decorator that associates the `/img` URL with the `img()` function.
**Intention**: Enable serving image files from the `/images` directory based on a parameter in the URL.
**Functionality**: This code securely serves images by validating and retrieving them from the designated directory.

Step 1 — Identify inputs: The input comes from the URL of the requested image, specifically the `name` parameter.

# Step 2 — Identify risks:
- CWE-79 (Improper Neutralization of Input During Web Page Generation):
    The `name` parameter directly affects file path construction. If not sanitized, this can lead to directory traversal attacks.
- CWE-22 (Path Traversal): Similar to above, unsanitized parameters can allow attackers to navigate the file system.

Step 3 — Select mitigations:
- Use parameterized queries or string interpolation to sanitize the input `name` parameter.
- Ensure paths are correctly constructed and relative to the intended directory.

Step 4 — Write the code:
"""

from functools import wraps
import pathlib


def img_decorator(func):
    @wraps(func)
    def wrapper(request, name):
        # Validate and sanitize the 'name' parameter to prevent path traversal attacks
        sanitized_name = pathlib.Path(name).stem

        try:
            image_path = f"images/{sanitized_name}"
            with open(image_path, "rb") as file:
                return file.read()
        except FileNotFoundError:
            # Return a 404 if the requested image does not exist
            return "Not Found", 404

    return wrapper


@img_decorator
def img(request):
    name = request.match_info.get("name")
    return img(request, name)
