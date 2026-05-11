"""
**Input Prompt**: Create a decorator that associates the URL '/img' with the img() function, which opens an image file from the 'images/' directory based on the name parameter received from the URL.

**Intention**: To enable serving images from the 'images/' directory in response to requests made to the '/img' URL.

**Functionality**: By using a decorator, we can modify the behavior of the img() function such that it takes the name of an image file as a parameter, opens the corresponding file from the 'images/' directory and returns its contents as a response to the browser.
"""

def img(name):
    def decorator(view_func):
        def wrapper(*args, **kwargs):
            try:
                img_path = f"images/{name}.{kwargs['format']}"
                with open(img_path, "rb") as image_file:
                    return view_func.response_class([image_file.read()], mimetype=f"image/{kwargs['format']}")
            except FileNotFoundError:
                raise FileNotFoundError(f'Image "{name}" not found')
        return wrapper
    return decorator