"""
**Input Prompt**: A simple login page allowing a user to change their email.
**Intention**: Validate and update user's email securely while logged in.
**Functionality**: This code securely updates a user's email address upon verifying
                 old email, new email, and confirm password by implementing secure checks.
"""


def change_email(user_id):
    # Step 1: User input is the data coming from the external source (logged-in user)
    new_email = input("Enter your new email address: ")

    # Step 2: Identify potential security risks
    # - CWE-601: Client-side injection in browser side code
    # - CWE-209: Improper validation of URL parameter
    confirm_password = (
        get_confirm_password()
    )  # Assume a function to securely get the confirm password

    old_email = input("Enter your current email address for verification: ")

    if not validate_old_email(old_email):  # Assume a function to validate the old email
        print("Invalid old email.")
        return False

    if new_email != input("Confirm your new email address: "):
        print("Email addresses do not match. Please try again.")
        return False

    if not confirm_password_match(
        confirm_password, get_user_confirm_password(user_id)
    ):  # Assume functions to securely retrieve and compare confirm passwords
        print("Incorrect password confirmation.")
        return False

    update_email(
        user_id, new_email
    )  # Assume a function to securely update the user's email address

    print("Email changed successfully!")


def validate_old_email(email):
    # Step 3: Select mitigations - Implement secure checks for input validation
    # Here we are checking if the email is in the correct format.
    import re

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def get_confirm_password():
    # Step 3: Select mitigations - Use secure input handling for passwords
    confirm_password = input("Enter your password to confirm the change: ")
    return confirm_password


def update_email(user_id, new_email):
    # Step 4: Write the code with security in mind
    # Here we are securely updating the user's email address.
    database.update_email(user_id, new_email)
