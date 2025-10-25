import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import PyQt5.QtCore as QtCore


class LoginPage(QWidget):
    def __init__(self, switch_to_dashboard):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(100, 100, 100, 100)

        title = QLabel("Login Page")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(
            "background-color: #1976d2; color: white; font-size: 16px; padding: 8px;")
        login_btn.clicked.connect(switch_to_dashboard)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn, alignment=QtCore.Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("background: #f5f5f5;")
