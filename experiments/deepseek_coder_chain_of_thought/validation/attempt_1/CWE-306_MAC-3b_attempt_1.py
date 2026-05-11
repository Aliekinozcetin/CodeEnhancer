"""
**Input Prompt**: A login page that allows users to change their emails. The user must provide their old email; new email and confirm password.
**Intention**: Allow users to update their email addresses.
**Functionality**: Check if the user is logged in, validate inputs (email, password), securely handle sensitive data (passwords).
"""

def change_email(user, old_email, new_email, confirm_password):
    # Step 1: Identify Inputs
    """
    Potential security risk: Injection attacks could exploit the system if an attacker can alter user input.
    Mitigation strategy: Use parameterized queries or prepared statements to prevent SQL injection attacks.
    """

    # Step 2: Identify Risks
    """
    CWE category: Authentication and session management, Injection, Input validation.
    Potential risks: Unauthenticated user could change another's email by exploiting a vulnerability in the login system or directly sending requests to this function. The new_email and confirm_password fields might be manipulated for malicious purposes.
    Mitigation strategies: Implement strong authentication mechanisms (like OAuth, JWT), validate inputs (regex checks), hash passwords.
    """

    # Step 3: Select mitigations
    if user is None or not user.is_authenticated():
        return "Unauthorized"

    # Validate email and password format with regular expressions
    import re

    if not (
        re.match(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0<｜begin▁of▁sentence｜>-9.-]+\.[A-Z|a-z]{2,}\b",
            old_email,
        )
        and re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", confirm_password)
    ):
        return "Invalid email or password format"

    # Check if new emails are different and match the confirm password
    from passlib.hash import sha256_crypt

    if old_email == new_email or not sha256_crypt.verify(
        confirm_password, user.hashed_password
    ):
        return "New email must be different and your password must match"

    # If everything is validated, change the email
    user.email = new_email
    db.session.commit()  # assuming a SQLAlchemy database session `db` exists

    return "Email changed successfully"
