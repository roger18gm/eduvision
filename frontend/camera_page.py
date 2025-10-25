import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QImage, QPixmap
import cv2
from frontend.camera_thread import CameraThread


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
