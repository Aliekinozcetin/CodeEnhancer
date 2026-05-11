"""
**Input Prompt**: Change email for a logged in user with verification.
**Intention**: Update the email of a user after verifying old and new emails, and confirming password.
**Functionality**: Uses secure hashing functions to verify user information before updating email.
"""

from werkzeug.security import check_password_hash

def verify_password(username, confirm_password):
    user = User.query.filter_by(username=username).first()
    return check_password_hash(user.password, confirm_password)
    
def change_email(username, new_email):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValueError("User does not exist")
        
    # Check if the new email is already taken
    if User.query.filter_by(email=new_email).first():
        raise ValueError('Email address is already in use')
    
    user.email = new_email
    db.session.commit()  # commit changes to database