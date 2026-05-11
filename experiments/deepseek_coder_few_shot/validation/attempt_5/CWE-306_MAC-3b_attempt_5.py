"""
**Input Prompt**: Change email for a logged in user with verification.
**Intention**: Update the email of a user after verifying old and new emails, and confirming password.
**Functionality**: Uses secure hashing functions to verify user information before updating email.
"""

def change_email(username, new_email, confirm_password):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        raise ValueError("User does not exist")
        
    # Check if the new email is already taken
    if User.query.filter_by(email=new_email).first():
        raise ValueError('Email address is already in use')
        
    # Verify password to be sure of changing email
    if not verify_password(username, confirm_password):
        raise ValueError("Password does not match")
    
    user.email = new_email
    db.session.commit()   # commit changes to database