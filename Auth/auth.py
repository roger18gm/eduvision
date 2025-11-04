import sqlite3
import bcrypt
import os
import sys


class Auth:
    def __init__(self, db_path="./database/eduvisiondb.db"):
        if getattr(sys, 'frozen', False):
            # Running as bundled exe
            print("Running as bundled executable")
            base_path = sys._MEIPASS
        else:
            # Running as script
            print("Running as script")
            base_path = os.path.dirname(
                os.path.dirname(__file__))  # Project root
        full_path = os.path.join(base_path, db_path)
        self.db_path = full_path

    def verify_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password, role_id FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()

        conn.close()

        if result:
            hashed_password, role_id = result
            # bcrypt needs both values as bytes
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                return {"username": username, "role_id": role_id}
        return None
