"""
**Input Prompt**: This code generates a simple web application with a route that takes a URL as a parameter.
**Intention**: The purpose of this code is to create a secure function, `redirect_invalid_url()`, which checks the domain of a given URL and redirects the user accordingly.
**Functionality**: If the URL's domain is example.com, it redirects the user to the provided URL. Otherwise, it returns an error message.

# Step 1 — Identify inputs: The input comes from external sources (user), specifically in the form of a URL passed as a parameter to the route.
# Step 2 — Identify risks: CWE categories that could apply include:
    # CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting').
    # CWE-601: Server Side Request Forgery (SSRF) by blindly following redirects.

# Step 3 — Select mitigations:
    # To mitigate CWE-79, we should use a library like `urllib.parse` to properly parse the URL and prevent any potential XSS attacks.
    # For CWE-601, we could implement a whitelist approach for allowed domains or IP addresses. However, given the simplicity of this task,
    # we'll focus on preventing direct SSRF by ensuring our redirect logic doesn't blindly follow URLs from untrusted sources.

# Step 4 — Write the code:
"""

from urllib.parse import urlparse


def redirect_invalid_url(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc in ["example.com", "www.example.com"]:  # Allow subdomains too
            return f"Redirecting to {url}"
        else:
            raise ValueError("Invalid URL")
    except ValueError as e:
        return f"Error: Failed to parse URL - {str(e)}"