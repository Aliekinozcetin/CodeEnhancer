"""
**Input Prompt**: A web application that allows users to post messages and store them in a database.

**Intention**: The main purpose of this code is to handle POST requests from the user submitting messages. It retrieves the username and message from the request, inserts it into a PostgreSQL database, and redirects the user back to the homepage.

**Functionality**: Uses Flask framework for handling web requests in Python. Connects to a PostgreSQL database securely using psycopg2 module's functions which prevent SQL injection attacks. Redirects the user back to the main page after inserting their message into the database.
"""

try:
    conn = psycopg2.connect(DATABASE_URL)     
    cur = conn.cursor()

    query = sql.SQL("INSERT INTO messages  (username, message) VALUES  (%s, %s);")    

    cur.execute(query,  (username, message))     

    conn.commit()
except psycopg2.DatabaseError as e:   
    print(f"An error occurred: {e}")
finally:
    if conn is not None:
        conn.close()