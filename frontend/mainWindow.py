import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
import cv2
from frontend.cameraThread import CameraThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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


class DashboardPage(QWidget):
    def __init__(self, switch_to_camera):
        super().__init__()

        # --- Main Layout ---
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)

        # --- Left: Matplotlib Graph ---
        graph_container = QVBoxLayout()
        graph_title = QLabel("Attendance Graph")
        graph_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; margin-bottom: 16px;")
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        graph_container.addWidget(graph_title)
        graph_container.addWidget(self.canvas)
        graph_container.addStretch()

        # --- Right: Controls ---
        controls_container = QVBoxLayout()
        title = QLabel("Dashboard Page")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 24px;")
        buildingComboBox = QComboBox()
        buildingComboBox.addItems(["Building A", "Building B", "Building C"])
        buildingComboBox.setStyleSheet("font-size: 16px; padding: 6px;")
        roomComboBox = QComboBox()
        roomComboBox.addItems(["Room 101", "Room 102", "Room 201"])
        roomComboBox.setStyleSheet("font-size: 16px; padding: 6px;")
        automation_btn = QPushButton("Go to Automation")
        automation_btn.setStyleSheet(
            "background-color: #43a047; color: white; font-size: 16px; padding: 8px; margin-top: 16px;")
        automation_btn.clicked.connect(self.switch_to_automation)
        camera_btn = QPushButton("Go to Camera")
        camera_btn.setStyleSheet(
            "background-color: #1976d2; color: white; font-size: 16px; padding: 8px; margin-top: 8px;")
        camera_btn.clicked.connect(switch_to_camera)

        controls_container.addWidget(title)
        controls_container.addWidget(buildingComboBox)
        controls_container.addWidget(roomComboBox)
        controls_container.addWidget(automation_btn)
        controls_container.addWidget(camera_btn)
        controls_container.addStretch()

        # --- Add to Main Layout ---
        main_layout.addLayout(graph_container, stretch=2)
        main_layout.addLayout(controls_container, stretch=1)

        self.setLayout(main_layout)
        self.setStyleSheet("background: #f5f5f5;")

        self.plot_sample_graph()

    def plot_sample_graph(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot([1, 2, 3, 4], [10, 20, 15, 25], marker='o')
        ax.set_title("Sample Attendance Graph")
        ax.set_xlabel("Day")
        ax.set_ylabel("Count")
        self.canvas.draw()

    def switch_to_automation(self):
        pass  # Placeholder for automation page switch


class CameraPage(QWidget):
    def __init__(self, back_to_dashboard):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(80, 60, 80, 60)
        layout.setSpacing(30)

        title = QLabel("Camera Page")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 24px;")

        self.video_label = QLabel()
        self.video_label.setFixedSize(640, 360)
        self.video_label.setStyleSheet(
            "background: #222; border-radius: 12px;")
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)

        self.count_label = QLabel("Count: 0")
        self.count_label.setAlignment(QtCore.Qt.AlignCenter)
        self.count_label.setStyleSheet(
            "font-size: 18px; color: #1976d2; margin-top: 16px;")

        self.toggle_button = QPushButton("Start Camera")
        self.toggle_button.setStyleSheet(
            "background-color: #1976d2; color: white; font-size: 16px; padding: 10px 24px; border-radius: 6px; margin-top: 24px;"
        )

        # --- Navigation Buttons ---
        nav_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(
            "background-color: #757575; color: white; font-size: 15px; padding: 8px 18px; border-radius: 6px;"
        )
        back_btn.clicked.connect(back_to_dashboard)

        prev_btn = QPushButton("Previous Camera")
        prev_btn.setStyleSheet(
            "background-color: #bdbdbd; color: #222; font-size: 15px; padding: 8px 18px; border-radius: 6px;"
        )

        next_btn = QPushButton("Next Camera")
        next_btn.setStyleSheet(
            "background-color: #bdbdbd; color: #222; font-size: 15px; padding: 8px 18px; border-radius: 6px;"
        )

        nav_layout.addWidget(back_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(next_btn)

        layout.addWidget(title)
        layout.addWidget(self.video_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.count_label)
        layout.addWidget(self.toggle_button, alignment=QtCore.Qt.AlignCenter)
        layout.addLayout(nav_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("background: #f5f5f5;")

        # --- State ---
        self.camera_thread = None
        self.camera_running = False

        # --- Signals ---
        self.toggle_button.clicked.connect(self.toggle_camera)

    # ---------------------
    # CAMERA CONTROL
    # ---------------------
    def toggle_camera(self):
        if not self.camera_running:
            self.start_camera()
        else:
            self.stop_camera()

    def start_camera(self):
        self.camera_thread = CameraThread()
        self.camera_thread.frame_ready.connect(self.update_frame)
        self.camera_thread.people_count.connect(self.update_count)
        self.camera_thread.start()

        self.camera_running = True
        self.toggle_button.setText("Stop Camera")

    def stop_camera(self):
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_thread.wait()
            self.camera_thread = None

        self.video_label.clear()
        self.count_label.setText("Count: 0")
        self.camera_running = False
        self.toggle_button.setText("Start Camera")

    # ---------------------
    # FRAME UPDATES
    # ---------------------
    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_image = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def update_count(self, count):
        self.count_label.setText(f"Count: {count}")

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduVision")
        self.resize(1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Pages
        self.login_page = LoginPage(self.show_dashboard)
        self.dashboard_page = DashboardPage(self.show_camera)
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
