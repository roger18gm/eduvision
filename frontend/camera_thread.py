from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np


class CameraThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)
    people_count = pyqtSignal(int)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = True

    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            count = self.detect_people(frame)
            self.frame_ready.emit(frame)
            self.people_count.emit(count)
        self.cap.release()

    def detect_people(self, frame):
        # Placeholder for your detection model
        return 0

    def stop(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
