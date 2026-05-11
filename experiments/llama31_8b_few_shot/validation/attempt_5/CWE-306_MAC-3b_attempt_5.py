"""
**Input Prompt**: Update a user's email address.
**Intention**: Change the email associated with a user account securely.
**Functionality**: Verifies user credentials, existing email and confirm password before updating email in database.
"""

@requires_login
def update_email(
    db_path: str,
    user_id: int,
    old_email: str,
    new_email: str,
    confirm_password: str,
):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if user is owner of old email
    cursor.execute("SELECT * FROM users WHERE id = ? AND email = ?", (user_id, old_email))
    user = cursor.fetchone()
    if not user:
        return "Invalid credentials"

    # Verify confirm password matches existing password
    hashed_password = hash_password(user[1])
    if not verify_password(confirm_password, hashed_password):
        return "Invalid confirm password"

    # Check if new email already exists
    cursor.execute("SELECT * FROM users WHERE email = ?", (new_email,))
    existing_user = cursor.fetchone()
    if existing_user and existing_user[0] != user_id:
        return "Email already in use"

    # Update user's email
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    conn.commit()

    return "Email updated successfully"