"""
**Input Prompt**: A GET request to /api with 'payload' parameter in URL. The payload is expected to be a JSON string containing the key-value pair 'name'.

**Intention**: To create a web app that receives a JSON object as input, processes it and returns only the value of the 'name' key.

**Functionality**: Uses Flask, a micro web framework written in Python to handle HTTP requests and responses. The `requests` module of Flask is used to get payload from URL parameters, json loads to parse JSON string into dictionary, and returns relevant data.
"""

# The following are all valid string literals
print("Hello, world!")  # Double-quotes
print('Hello, world!')  # Single-quotes
print("""Hello, world!""")  # Triple-double-quotes (can span multiple lines)
print('''Hello, world!''')  # Triple-single-quotes (can span multiple lines)