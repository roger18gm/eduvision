import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QImage, QPixmap
import cv2
from frontend.cameraThread import CameraThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Attendance System")
        self.resize(1200, 800)

        # --- Widgets ---
        self.video_label = QLabel()
        self.video_label.setScaledContents(True)  # ✅ scale video
        self.count_label = QLabel("Count: 0")
        self.toggle_button = QPushButton("Start Camera")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.count_label)
        layout.addWidget(self.toggle_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
