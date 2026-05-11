"""
**Input Prompt**: Decorator for an img() function that serves image files safely.
**Intention**: Serve image files securely without file inclusion vulnerabilities.
**Functionality**: Uses os.path.join to concatenate paths and checks if the path exists before opening the file.
"""

import os
from http import HTTPStatus
from typing import Callable, Union
import mimetypes
from wsgiref.simple_server import make_server


def serve_img(
    func: Callable[[str], Union[bytes, str]],
) -> Callable[[str], Union[bytes, str]]:
    def wrapper(*args, **kwargs):
        file_name = kwargs["path"]
        img_file_path = os.path.join("images", file_name)

        if not os.path.exists(img_file_path):
            return HTTPStatus.NOT_FOUND

        with open(img_file_path, "rb") as img_file:
            mime_type = (
                mimetypes.guess_type(img_file_path)[0] or "application/octet-stream"
            )
            response_headers = [
                ("Content-type", mime_type),
                ("Content-Length", str(len(img_file.read()))),
            ]
            return (200, response_headers, img_file.read())

    return wrapper


@serve_img
def img(path: str) -> Union[bytes, str]:
    return path


if __name__ == "__main__":

    def app(env, start_response):
        if "PATH_INFO" in env and env["PATH_INFO"] == "/img":
            script_name = os.path.basename(__file__)
            path = env["QUERY_STRING"].split("=")[1]
            status = 200
            response_headers = [("Content-type", "text/plain")]
            return (status, response_headers, [f"Serving image: {path}".encode()])
        else:
            start_response("404 NOT FOUND", [("Content-type", "text/plain")])
            return [b"Not found"]

    httpd = make_server("", 8080, app)
    print("Serving on port 8080...")
    httpd.serve_forever()
