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
        self.dashboard_page = DashboardPage(self.db, self.show_camera)
        self.camera_page = CameraPage(self.show_dashboard)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.camera_page)

        self.show_login()

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_page)

    def show_camera(self):
        self.stacked_widget.setCurrentWidget(self.camera_page)
