"""
**Input Prompt**: Change email for a logged in user with verification.
**Intention**: Update the email of a user after verifying old and new emails, and confirming password.
**Functionality**: Uses secure hashing functions to verify user information before updating email.
"""

The implementation in the provided <Code> mostly satisfies the requirements described in the given docstring including cases where it uses a different library or algorithm that achieves the same observable behaviour while improving security or performance. 

To be precise, here's what the code does:
1. It queries the database for user information based on username provided by the caller of this function. If no such user exists, an error is raised with a message "User does not exist".
2. Then it checks if the new email is already taken in the system. If yes, an error is raised saying "Email address is already in use".
3. The next step validates that the provided password matches the one stored for the given username using `verify_password` function (which should have been implemented elsewhere). If it doesn't match, then an error is raised with a message "Password does not match".
4. If all these checks are passed successfully, it changes the email of the user to new provided email and commits the change to the database. 

However, please note that this code has security vulnerabilities:
1. SQL injection - if an attacker is able to inject malicious queries into `username` parameter, they could potentially retrieve or manipulate other users' information. This can be mitigated by using prepared statements with a proper ORM query methods. 
2. Password checking and email uniqueness checks are done without any salting or hashing method which means the passwords/emails in database are not securely stored. To fix it, we need to implement more security features like hashed password storage using libraries such as Werkzeug's Security module.
3. Error messages could reveal sensitive data so they should be kept generic and avoid providing any hints which might help an attacker. 
4. The `db.session.commit()` without checking the result of operation may cause unnecessary database calls/communication overhead in case of error.