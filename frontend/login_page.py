import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtCore
from Auth.auth import Auth 


class LoginPage(QWidget):
    def __init__(self, switch_to_dashboard):
        super().__init__()
        self.auth = Auth()  # ✅ create an Auth instance
        self.switch_to_dashboard = switch_to_dashboard

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(100, 100, 100, 100)

        title = QLabel("Login Page")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Username label + input
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        # Password label + input
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(
            "background-color: #1976d2; color: white; font-size: 16px; padding: 8px;"
        )
        login_btn.clicked.connect(self.handle_login)

        layout.addWidget(title)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("background: #f5f5f5;")

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user = self.auth.verify_user(username, password)

        if user:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            self.switch_to_dashboard()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
