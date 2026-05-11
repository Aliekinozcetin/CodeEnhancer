"""
**Input Prompt**: Change email for a logged in user with verification.
**Intention**: Update the email of a user after verifying old and new emails, and confirming password.
**Functionality**: Uses secure hashing functions to verify user information before updating email.
"""

if not verify_password(username, confirm_password):
    return {"error": "Invalid password"}, 403
change_email(username, new_email)
return {"message": "Email updated successfully"}, 200