"""
Input Prompt:
Intention:
Functionality:
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

# Generate salt once and store it securely (e.g., in environment variables)
salt = bcrypt.gensalt().decode('utf-8')

engine = create_engine('sqlite:///users.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)

    def __repr__(self):
        return f"User(username='{self.username}', hashed_password='{self.hashed_password}')"

Base.metadata.create_all(engine)

with engine.connect() as connection:
    # Ensure that the password is correctly inserted into the database
    user_data = {'username': username, 'hashed_password': hashed_password.decode('utf-8')}
    connection.execute(User.__table__.insert(), **user_data)