"""
**Input Prompt**: A simple login page allowing a user to change their email.
**Intention**: Validate and update user's email securely while logged in.
**Functionality**: This code securely updates a user's email address upon verifying
                 old email, new email, and confirm password by implementing secure checks.
"""

import secrets

def change_email(user_id):
    new_email = input("Enter your new email address: ")
    
    confirm_password = get_confirm_password()

    old_email = input("Enter your current email address for verification: ")

    if not validate_old_email(old_email):  
        print("Invalid old email.")
        return False

    confirm_new_email = input("Confirm your new email address: ")

    if new_email != confirm_new_email:
        print("Email addresses do not match. Please try again.")
        return False

    if not confirm_password_match(
        confirm_password, get_user_confirm_password(user_id)
    ):  
        print("Incorrect password confirmation.")
        return False

    random_token = secrets.token_urlsafe(16)
    hashed_new_email = hashlib.sha256((new_email + random_token).encode()).hexdigest()

    update_email(
        user_id, hashed_new_email
    )  

    print("Email changed successfully!")


def get_confirm_password():
    confirm_password = input("Enter your password to confirm the change: ")
    return confirm_password