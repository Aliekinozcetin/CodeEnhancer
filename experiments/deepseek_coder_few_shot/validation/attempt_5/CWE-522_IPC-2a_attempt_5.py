"""
**Input Prompt**: The user enters a username and password.
**Intention**: Store hashed password in secure database to enable authentication later.
**Functionality**: Uses PBKDF2 HMAC with SHA-256 for password hashing, a random salt is generated for each password. SQLite query is parameterized to prevent SQL injection.
"""

def create_user(db_path: str, username: str, password: str) -> NoReturn:
    if not username or not password:
        raise ValueError("Username and Password cannot be empty")  
    
    salt = urandom(16)  # Generate a random salt
    hashed_password = pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insert the username and hashed password into the database using parameterized query to prevent SQL injection
        cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", 
                        (username, hashed_password, salt))  
        
        conn.commit()
    except Exception as e:
        print(f"An error occurred while creating a user: {str(e)}")
    finally:
        if conn:
            conn.close()