"""
Input Prompt:
The program will take an input in two parts - a username and a password.

Intention:
This script aims at implementing a basic login system. The inputs are provided by the user, which includes their username and password.

Functionality:
The program checks if the username exists in the database. If it does, it will check if the given password matches the one stored in the database.
If both conditions are met, the user is redirected to the home page. Else, an error message is returned stating 'Incorrect Username or Password'.
"""


def login(username, password):
    # This would be a part of actual implementation which checks if username exists in database
    username_exists = False

    # This would be the query to get correct password from database. For simplicity, we'll just return a dummy value.
    correct_password = "dummypassword"

    if username and password:
        if username_exists:
            if password == correct_password:
                print(
                    "Redirecting to home page..."
                )  # This would be replaced with actual redirect in real application
            else:
                return "Incorrect Username or Password."
        else:
            return "Username does not exist."
    else:
        return "Both username and password are required."
