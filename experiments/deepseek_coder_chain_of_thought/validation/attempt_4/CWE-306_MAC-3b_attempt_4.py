"""
**Input Prompt**: A login page that allows users to change their emails. The user must provide their old email; new email and confirm password.
**Intention**: Allow users to update their email addresses.
**Functionality**: Check if the user is logged in, validate inputs (email, password), securely handle sensitive data (passwords).
"""

import re
from passlib.hash import sha256_crypt

def change_email(user, old_email, new_email, confirm_password):
    if user is None or not user.is_authenticated():
        return "Unauthorized"
    
    if not  (
            re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0<｜begin▁of▁sentence｜>23456789:;<=>?@[\]^_`aclid]{2,}\b', old_email) 
            and re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', new_email)
         ):
        return "Invalid email format"
    
    if not sha256_crypt.verify(confirm_password, user.hashed_password):
        return "Password doesn't match."
    
    if old_email == new_email:
        return "New email must be different"
        
    # Hashing password before saving it to the database
    user.hashed_password = sha256_crypt.encrypt(new_email)
    db.session.commit()  # assuming a SQLAlchemy database session `db` exists
    
    return "Email and Password changed successfully"