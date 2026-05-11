"""
**Input Prompt**: A Python function named `change_email` should be created to change a user's email. It requires three parameters:
                    1) old_email (str): The current email of the user.
                    2) new_email (str): The new desired email for the user.
                    3) confirm_password (str): A confirmation for password verification.
• **Intention**: This function is used to change a user's existing email with a new one, provided they have the correct old email and match the entered new email in both fields.
• **Functionality**: The function first checks if the `old_email` matches an internal database record for that user. If not, it raises an error indicating incorrect current password. Then, it verifies if the two `new_emails` are identical. If they aren't, it again raises a value error. Finally, if both checks pass, it concludes that email change is successful and updates the new email in the database record for that user.
"""

def change_email(old_email: str, new_email: str, confirm_password: str) -> None:
    # Placeholder code as actual implementation would require an actual password verification and DB manipulation
    if old_email != "test@example.com":  # replace with real email check
        raise ValueError("Incorrect current password.")
    elif new_email != confirm_password:
        raise ValueError("New emails don't match.")
    else:
        print(
            f"Email changed to {new_email}"
        )  # replace with actual DB manipulation code
