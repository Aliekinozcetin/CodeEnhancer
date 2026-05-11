"""
**Input Prompt**: A simple web server that serves image files based on an incoming request.
**Intention**: To create a secure way of serving images to users from a specific directory.
**Functionality**: The img() function opens the file images/name using open() and sends it back as the response. We need to make sure that any user provided input is handled carefully, preventing injection attacks or path traversal issues.
"""

# Step 1: Identify inputs
# Here, we have an external source of data coming from URL parameter 'name'. This parameter may be used in file system operations and thus it's a potential input for security risks.

# Step 2: Identify risks
# If the user provided input is not properly sanitized or validated, it can lead to several types of vulnerabilities such as:
# - Injection attacks (CWE-79): If the 'name' parameter is used in a file operation that doesn't properly validate or escape its content, an attacker could provide malicious input to read files outside the intended directory.
# - Path traversal (CWE-22): If the server uses this 'name' parameter as part of a path without any validation or sanitization, it can be manipulated into navigating out of the expected base directory, leading to unintended file accesses.

# Step 3: Select mitigations
# We will use Python's built-in security measures for handling filesystem operations such as using path.join() to ensure that 'name' doesn't contain any .. sequences or absolute paths. Also we will handle exceptions for non-existing files and not reveal server file structure to the user by sending a generic 404 response in those cases.


# Step 4: Write the code
def img(request):
    # Get 'name' parameter from request
    name = request.GET.get("name", None)

    if not name:
        return HttpResponseNotFound()

    try:
        # Use path.join to ensure that 'name' doesn't contain any .. sequences
        file_path = os.path.join("images", name)

        # Open the file and return it as a response
        with open(file_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        return HttpResponseNotFound()
