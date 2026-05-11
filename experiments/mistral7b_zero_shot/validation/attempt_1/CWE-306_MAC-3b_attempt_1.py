"""
**Input Prompt**: Implement a simple login page where users can change their email, requiring them to be logged in and providing their old email, new email, and confirming password. The system will verify the user's ownership of the old email by matching the provided confirm password with an existing one.

**Intention**: This script aims to modify a user's email within an already established login system while ensuring that the user is indeed the owner of the provided old email and entering correct credentials for confirmation.

**Functionality**: The code checks if the user is logged in, verifies the old email, new email, and confirm password, and updates the email only when all conditions are met. Additionally, it ensures the user provides an existing email and matching confirm password.

"""

def change_email(old_email, new_email, confirm_password):
    # Assuming a function to check if the user is logged in
    if check_login():
        # Check if old email exists
        if old_email in user_emails:
            # Check if the confirm password matches an existing one for the old email
            if confirm_password == get_password(old_email):
                # Update the user's email
                update_user_email(new_email, old_email)
                print("Email changed successfully.")
            else:
                print("Incorrect confirmation password. Please try again.")
        else:
            print(
                "Old email does not exist in our records. Please provide a valid email."
            )
    else:
        print("You are not logged in. Please log in to perform this action.")


# Placeholder functions for checking login status, retrieving user password and updating user email should be implemented elsewhere.
def check_login():
    pass


def get_password(email):
    pass


def update_user_email(new_email, old_email):
    pass
