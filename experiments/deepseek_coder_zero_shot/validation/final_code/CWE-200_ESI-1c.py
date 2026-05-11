"""
Input Prompt:
The program will take an input in two parts - a username and a password.

Intention:
This script aims at implementing a basic login system. The inputs are provided by the user, which includes their username and password.

Functionality:
The program checks if the username exists in the database. If it does, it will check if the given password matches the one stored in the database.
If both conditions are met, the user is redirected to the home page. Else, an error message is returned stating 'Incorrect Username or Password'.
"""

import re
from my_other_module import my_function

def is_integer(value):
    return str(value).isdigit()

class MyClass:
    def __init__(self, string):
        self.string = string

    def get_strings(self):
        # This line was causing the syntax error
        if re.match("^[a-zA-Z]*$", self.string):
            return [self.string]
        else: 
            return []