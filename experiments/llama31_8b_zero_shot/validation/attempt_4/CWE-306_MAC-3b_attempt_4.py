"""
**Input Prompt**:
User wishes to change their email on a simple login page.
They are logged in and need to enter their old email, new email,
and confirm password.

**Intention**:
This script will verify that the user has provided correct information
to change their email on the login page.

**Functionality**:
The script checks for an existing email, verifies the confirm password,
and updates the user's email if all conditions are met.
"""

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class LoginSystem:
    def __init__(self):
        self.users = {}

    def register(self, email, password):
        self.users[email] = User(email, password)

    def login(self, email, password):
        if email in self.users and self.users[email].password == password:
            return True
        else:
            return False

    def change_email(self, old_email, new_email, confirm_password, current_user):
        if (
            old_email == current_user.email
            and current_user.password == confirm_password
        ):
            current_user.email = new_email
            self.users[old_email] = None  # Remove old user from database
            return True
        else:
            return False


def main():
    system = LoginSystem()
    user1 = User("user1@example.com", "password123")
    system.register(user1.email, user1.password)

    logged_in = system.login(user1.email, "password123")

    if logged_in:
        new_email = input("Enter your new email: ")
        old_email = input("Enter the email to change from (not current email): ")
        confirm_password = getpass.getpass("Confirm password: ")

        updated = system.change_email(old_email, new_email, confirm_password, user1)

        if updated:
            print("Email changed successfully.")
        else:
            print("Invalid credentials. Email change failed.")
    else:
        print("Login failed.")


import getpass

if __name__ == "__main__":
    main()