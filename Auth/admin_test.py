import sqlite3
import bcrypt

conn = sqlite3.connect("./database/eduvisiondb.db")
cursor = conn.cursor()

username = "admin2"
password = "1234".encode("utf-8")
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# Assuming a role exists (like Admin in the role table)
cursor.execute("SELECT role_id FROM role WHERE name = ?", ("Admin",))
role_id = cursor.fetchone()[0]

cursor.execute("""
    INSERT INTO user (username, password, role_id)
    VALUES (?, ?, ?)
""", (username, hashed, role_id))

conn.commit()
conn.close()
