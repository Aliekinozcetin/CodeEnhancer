"""
**Input Prompt**: Update a user's email address.
**Intention**: Change the email associated with a user account securely.
**Functionality**: Verifies user credentials, existing email and confirm password before updating email in database.
"""

import sqlite3
from passlib.context import CryptContext
from functools import wraps

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in (replace with actual authentication logic)
        if not kwargs.get("user_logged_in"):
            return "You must be logged in to update your email."
        return f(*args, **kwargs)

    return decorated_function


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hashed counterpart"""
    return pwd_context.verify(password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a password for storage"""
    return pwd_context.hash(password)


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

    # Verify confirm password matches existing password (use verify_password instead)
    if not pwd_context.verify(confirm_password, user[1]):
        return "Invalid confirm password"

    # Check if new email already exists
    cursor.execute("SELECT * FROM users WHERE email = ?", (new_email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return "Email already in use"

    # Update user's email
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    conn.commit()

    return "Email updated successfully"