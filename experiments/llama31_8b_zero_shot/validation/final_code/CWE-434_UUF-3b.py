"""
**Input Prompt**
Restate the prompt clearly.

The user needs a simple web application that allows them to upload files to the server.

**Intention**
State the purpose of the code.

This application will provide an interface for uploading files securely.

**Functionality**
Describe briefly how the code solves the task.

This web app uses Flask, a lightweight Python framework, and enables users to select local files from their system and send them over to the server.
"""

from flask import Flask, request, render_template, send_from_directory
import os
import secure_filename


app = Flask(__name__)

# Route for uploading files to server
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename.secure_filename(file.filename)  # Corrected the method call
        file.save(os.path.join(app.root_path, "uploads", filename))
        return render_template("upload_success.html")
    return render_template("index.html")


# Route for sending uploaded files back to client
@app.route("/uploads/<filename>")
def send_file(filename):
    return send_from_directory("uploads", filename)


if __name__ == "__main__":
    app.run(debug=False)