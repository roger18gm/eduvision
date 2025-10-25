import sqlite3
import bcrypt

class Auth:
    def __init__(self, db_path="C:/Users/vinni/OneDrive/Documents/Hackathon Fall 2025/eduvision/database/eduvisiondb.db"):
        self.db_path = db_path

    def verify_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT password, role_id FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()

        conn.close()

        if result:
            hashed_password, role_id = result
            # bcrypt needs both values as bytes
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                return {"username": username, "role_id": role_id}
        return None
