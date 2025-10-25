import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from Auth.auth import Auth 


class LoginPage(QWidget):
    def __init__(self, switch_to_dashboard):
        super().__init__()
        self.auth = Auth()  # ✅ create an Auth instance
        self.switch_to_dashboard = switch_to_dashboard

        # Main layout with centered glassmorphism card
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create glassmorphism login card
        self.login_card = self.create_glassmorphism_card()
        main_layout.addStretch()
        main_layout.addWidget(self.login_card, 0, Qt.AlignCenter)
        main_layout.addStretch()
        
        # Add vertical stretch for centering
        v_layout = QVBoxLayout()
        v_layout.addStretch()
        v_layout.addLayout(main_layout)
        v_layout.addStretch()
        
        self.setLayout(v_layout)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0a0a, stop:0.3 #1a1a2e, stop:0.7 #16213e, stop:1 #0f3460);
            }
        """)
    
    def create_glassmorphism_card(self):
        """Create a glassmorphism login card."""
        card = QFrame()
        card.setFixedSize(450, 500)
        card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Futuristic title with glow effect
        title = QLabel("EduVision")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #00d4ff;
                background: transparent;
            }
        """)
        
        subtitle = QLabel("AI-Powered Campus Analytics")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: rgba(255, 255, 255, 0.7);
                background: transparent;
                margin-bottom: 20px;
            }
        """)
        
        # Username section
        username_label = QLabel("Username")
        username_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #ffffff;
                font-weight: 500;
                margin-bottom: 5px;
            }
        """)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(0, 212, 255, 0.3);
                border-radius: 12px;
                color: #ffffff;
                font-size: 16px;
                padding: 20px;
                margin-bottom: 10px;
                min-height: 25px;
            }
            QLineEdit:focus {
                border: 2px solid #00d4ff;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
        """)
        
        # Password section
        password_label = QLabel("Password")
        password_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #ffffff;
                font-weight: 500;
                margin-bottom: 5px;
            }
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(0, 212, 255, 0.3);
                border-radius: 12px;
                color: #ffffff;
                font-size: 16px;
                padding: 20px;
                margin-bottom: 10px;
                min-height: 25px;
            }
            QLineEdit:focus {
                border: 2px solid #00d4ff;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
        """)
        
        # Login button with futuristic styling
        login_btn = QPushButton("LOGIN")
        login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099cc);
                border: none;
                border-radius: 12px;
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                padding: 18px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00e5ff, stop:1 #00b3e6);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0099cc, stop:1 #007399);
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        
        # Add all widgets to layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addStretch()
        
        card.setLayout(layout)
        return card

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user = self.auth.verify_user(username, password)

        if user:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            self.switch_to_dashboard()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
