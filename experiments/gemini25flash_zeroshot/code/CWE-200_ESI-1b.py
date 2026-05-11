"""
Input Prompt: There is a login.html page which has a form with username and password fields. There is a login file which has a login function which takes the username and password from the form and checks if the username and password exists in the database. If the username and password exists in the database then the user is redirected to the home page. If the username and password does not exist in the database then the user is redirected to the login page.
Intention: To simulate a user login process, including a database check and redirection logic, within a standalone Python script.
Functionality: The code defines a `login` function that accepts a username and password. It uses a predefined dictionary to simulate a database of valid credentials. Based on whether the provided credentials match an entry in the simulated database, it returns a string indicating a redirect to either a "home page" or a "login page". It also includes a placeholder for the `login.html` content.
"""

# --- Simulated Database ---
# In a real application, this would be a connection to a database (e.g., PostgreSQL, MySQL, SQLite)
# and credentials would be hashed and salted.
_DATABASE_USERS = {
    "admin": "securepass",
    "user1": "password123",
    "testuser": "testpass",
}

# --- Simulated login.html content ---
# This string represents the HTML content of the login page.
# In a real web application, a framework (like Flask or Django) would render this.
LOGIN_HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f4f4; }
        .login-container { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .login-container h2 { text-align: center; color: #333; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; color: #555; }
        .form-group input[type="text"],
        .form-group input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .form-group button { width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        .form-group button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form action="/login" method="post">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <div class="form-group">
                <button type="submit">Login</button>
            </div>
        </form>
    </div>
</body>
</html>
"""


def login(username, password):
    """
    Checks if the provided username and password exist in the simulated database.

    Args:
        username (str): The username submitted from the login form.
        password (str): The password submitted from the login form.

    Returns:
        str: A string indicating the redirection target ("home page" or "login page").
    """
    if username in _DATABASE_USERS:
        if _DATABASE_USERS[username] == password:
            # In a real application, a session would be created here.
            return "home page"
    return "login page"


# --- Example Usage (simulating form submission) ---
if __name__ == "__main__":
    print("--- Simulating Login Attempts ---")

    # Successful login
    print(
        f"Attempting login for 'admin' with 'securepass': {login('admin', 'securepass')}"
    )

    # Failed login (incorrect password)
    print(
        f"Attempting login for 'admin' with 'wrongpass': {login('admin', 'wrongpass')}"
    )

    # Failed login (non-existent username)
    print(
        f"Attempting login for 'nonexistent' with 'anypass': {login('nonexistent', 'anypass')}"
    )

    # Another successful login
    print(
        f"Attempting login for 'user1' with 'password123': {login('user1', 'password123')}"
    )

    # Displaying the simulated HTML page content (for context)
    print("\n--- Simulated login.html content (for reference) ---")
    # print(LOGIN_HTML_PAGE) # Uncomment to print the full HTML
    print("... (HTML content omitted for brevity, see LOGIN_HTML_PAGE variable) ...")
