import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
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
        self.setWindowTitle("EduVision")
        self.resize(1200, 800)
        self.db = Database()

        self.stacked_widget = QStackedWidget()
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
