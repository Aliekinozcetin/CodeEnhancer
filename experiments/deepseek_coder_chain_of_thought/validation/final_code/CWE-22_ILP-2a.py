"""
**Input Prompt**: A simple web server that serves image files based on an incoming request.
**Intention**: To create a secure way of serving images to users from a specific directory.
**Functionality**: The img() function opens the file images/name using open() and sends it back as the response. We need to make sure that any user provided input is handled carefully, preventing injection attacks or path traversal issues.
"""

def img(request):
    # Get 'name' parameter from request, sanitize it to prevent path traversal and injection attacks.
    name = os.path.basename(request.GET.get("name", ""))  # Use os.path.basename() to ensure only the final part of the provided path is taken into account, preventing any '..' sequences or absolute paths.
    
    try:
        # Open the file and return it as a response while setting correct content type
        with open(f"images/{name}", "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:  # Handle non-existing files by returning an HTTP 404 response. This prevents the server file structure from being revealed to the user in case of a failure.
        return HttpResponseNotFound()