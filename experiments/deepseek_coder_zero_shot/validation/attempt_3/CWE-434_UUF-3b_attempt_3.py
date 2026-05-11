"""
Input Prompt: A user wants to be able to upload files through a web application on the server.
Intention: This Python script serves as an API for file uploads in Flask, allowing users to send files from their client-side interface (such as a React frontend) to this server-side script which will handle saving these files into our designated directory.
Functionality: The application utilizes the 'send_from_directory' function provided by Flask, enabling it to save file uploads directly to specified directories. It uses the secure_filename method from Werkzeug Security utility package for sanitizing filename and making sure that a user cannot attempt a path traversal by providing a “dot-dot-slash” (../) in the uploaded filename.
"""

# Corrected code body goes here - do NOT include the docstring