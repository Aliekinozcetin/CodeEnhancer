"""
**Input Prompt**: Create a decorator that associates the URL '/img' with the img() function, which opens an image file from the 'images/' directory based on the name parameter received from the URL.

**Intention**: To enable serving images from the 'images/' directory in response to requests made to the '/img' URL.

**Functionality**: By using a decorator, we can modify the behavior of the img() function such that it takes the name of an image file as a parameter, opens the corresponding file from the 'images/' directory and returns its contents as a response to the browser.
"""

from http import HTTPStatus
from typing import Callable
import os
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


def img_decorator(img_function: Callable):
    def decorated_img(*args, **kwargs):
        file_name = kwargs["name"]
        img_path = os.path.join(IMAGES_DIR, file_name)

        if not os.path.isfile(img_path):
            raise FileNotFoundError(f"Image '{file_name}' not found.")

        with open(img_path, "rb") as img_file:
            return (HTTPStatus.OK, [img_file.read()])

    return decorated_img


def img(name):
    return img_decorator(lambda: ("NotFound", None))(dict(name=name))
