import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QFont, QPalette, QColor, QLinearGradient, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
import cv2
from frontend.camera_thread import CameraThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from frontend.camera_page import CameraPage
from frontend.dashboard_page import DashboardPage
from frontend.login_page import LoginPage
from frontend.automation_page import AutomationPage
from database.db_repository import Database



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduVision - AI-Powered Campus Analytics")
        self.resize(1400, 900)
        self.setMinimumSize(1200, 800)
        self.db = Database()
        
        # Apply futuristic theme
        self.apply_futuristic_theme()
        
        # Create animated background
        self.create_animated_background()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background: transparent;
                border: none;
            }
        """)
        self.setCentralWidget(self.stacked_widget)

        # Pages
        self.login_page = LoginPage(self.show_dashboard)
        self.dashboard_page = DashboardPage(
            self.db, self.show_camera, self.show_automation)
        self.camera_page = CameraPage(self.db, self.show_dashboard)
        self.automation_page = AutomationPage(
            self.show_dashboard, self.get_snapshot_data)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.camera_page)
        self.stacked_widget.addWidget(self.automation_page)

        self.show_login()

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_page)

    def show_camera(self):
        building_id = self.dashboard_page.selected_building_id
        room_id = self.dashboard_page.selected_room_id
        self.camera_page.set_location(building_id, room_id)
        self.stacked_widget.setCurrentWidget(self.camera_page)

    def show_automation(self):
        self.stacked_widget.setCurrentWidget(self.automation_page)

    def get_snapshot_data(self):
        """Get current snapshot data from camera page."""
        # This will be called by the automation scheduler
        # For now, return mock data - in real implementation,
        # this would get data from the camera page
        from datetime import datetime
        return {
            'people_count': 0,  # Will be updated by camera page
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'datetime_obj': datetime.now()
        }
    
    def apply_futuristic_theme(self):
        """Apply a futuristic dark theme to the application."""
        # Set the main window style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0a0a, stop:0.3 #1a1a2e, stop:0.7 #16213e, stop:1 #0f3460);
                color: #ffffff;
            }
            
            QWidget {
                background: transparent;
                color: #ffffff;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00d4ff, stop:1 #0099cc);
                border: 2px solid #00d4ff;
                border-radius: 8px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00e5ff, stop:1 #00b3e6);
                border: 2px solid #00e5ff;
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0099cc, stop:1 #007399);
            }
            
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid #00d4ff;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                padding: 10px;
                selection-background-color: #00d4ff;
            }
            
            QLineEdit:focus {
                border: 2px solid #00e5ff;
            }
            
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid #00d4ff;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px;
                min-width: 100px;
            }
            
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #00d4ff;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background: rgba(26, 26, 46, 0.95);
                border: 2px solid #00d4ff;
                border-radius: 8px;
                color: #ffffff;
                selection-background-color: #00d4ff;
            }
            
            QLabel {
                color: #ffffff;
                background: transparent;
            }
            
            QTableWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid #00d4ff;
                border-radius: 8px;
                color: #ffffff;
                gridline-color: #00d4ff;
                selection-background-color: rgba(0, 212, 255, 0.3);
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(0, 212, 255, 0.2);
            }
            
            QTableWidget::item:selected {
                background: rgba(0, 212, 255, 0.3);
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00d4ff, stop:1 #0099cc);
                color: #ffffff;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
            
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid #00d4ff;
                border-radius: 8px;
                color: #ffffff;
                font-weight: bold;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QSpinBox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid #00d4ff;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px;
            }
            
            QSpinBox:focus {
                border: 2px solid #00e5ff;
            }
        """)
    
    def create_animated_background(self):
        """Create an animated background effect."""
        # This could be enhanced with actual animated elements
        # For now, we'll use CSS gradients and effects
        pass
