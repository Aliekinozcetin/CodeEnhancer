"""
**Input Prompt**:
The user enters the username and password in the login page. The username and password are sent to the login function.

**Intention**:
This code aims to validate a user's credentials by checking their existence in a database and comparing them with stored passwords.

**Functionality**:
The login function checks if a given username exists, then verifies its corresponding password against the one stored in the database. If both match, it redirects the user to the home page.
"""

def login(username, password):
    # Simulate database query
    db_users = {"user1": "password1", "user2": "password2"}

    if username in db_users:
        if db_users[username] == password:
            print("Redirecting to home page")
        else:
            print("Incorrect password")
    else:
        print("Username does not exist")


def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    login(username, password)


if __name__ == "__main__":
    main()
