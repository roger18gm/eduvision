import sqlite3
import bcrypt

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from database import Database  # your Database class file

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("EduVision Login")
        self.resize(300, 200)
        self.setup_ui()

    def setup_ui(self):
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.handle_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)

    def handle_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        user = self.db.verify_user(username, password)
        if user:
            QMessageBox.information(
                self, "Welcome",
                f"Login successful!\n\nUser: {user['username']}\nRole: {user['role_name']}"
            )
            # 👉 You could open your main app window here depending on the role
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
