import sqlite3, random, string
from datetime import datetime, timedelta

import os

from lib_functions import encode, get_salt
from db_functions import *

from db_setup import setup_db


class CurrentUser:
    def __init__(self):
        super().__init__()

        setup_db()
        self.logout_user()

    # user related
    def login_user(self, username, password):
        # Retrieve the user's salt and hashed password from the database
        # query = "SELECT username, salt, password, role, office FROM users WHERE username = ?"
        result = fetchone(
            table="users",
            condition=f"username='{username}'",
        )

        if result is not None:
            username, hashed_password, salt, role, office = result

            # Hash the provided password with the retrieved salt
            input_hashed_password = encode(password, salt)

            # Compare the hashed passwords
            if input_hashed_password == hashed_password:
                # Passwords match
                self.username = username
                self.role = role
                self.office = office
                # insert("sessions")

        # Login failed, return None
        return None

    def logout_user(self):
        self.username = None
        self.role = None
        self.office = None

    def build(self):
        return self
