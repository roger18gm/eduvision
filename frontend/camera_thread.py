from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import sys
import os

# Add the project root to the path to import vision modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vision.yolo_people_counter import PeopleCounter
from vision.iphone import get_available_cameras, switch_camera


class CameraThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)
    people_count = pyqtSignal(int)
    fps_updated = pyqtSignal(float)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = True
        self.people_counter = PeopleCounter()
        self.available_cameras = get_available_cameras()
        self.switch_requested = False
        self.cap = None

    def run(self):
        while self.running:
            # Check if camera switch was requested
            if self.switch_requested:
                self.switch_to_next_camera()
                self.switch_requested = False
            
            # Initialize or reinitialize camera
            if self.cap is None or not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self.camera_index)
                
                if not self.cap.isOpened():
                    print(f"Error: Could not open camera {self.camera_index}.")
                    # Try next camera if available
                    if self.switch_to_next_camera():
                        continue
                    else:
                        break

            ret, frame = self.cap.read()
            if not ret:
                print(f"Error reading from camera {self.camera_index}")
                # Try to switch to next camera
                if self.switch_to_next_camera():
                    continue
                else:
                    break
            
            # Use the PeopleCounter to detect and count people
            annotated_frame = self.people_counter.detect_and_count(
                frame, 
                current_camera=self.camera_index, 
                available_cameras=self.available_cameras
            )
            
            # Emit the annotated frame and people count
            self.frame_ready.emit(annotated_frame)
            self.people_count.emit(self.people_counter.current_count)
            self.fps_updated.emit(self.people_counter.fps)
            
        if self.cap and self.cap.isOpened():
            self.cap.release()

    def switch_camera(self):
        """Request to switch to the next available camera"""
        if len(self.available_cameras) <= 1:
            return False
        
        self.switch_requested = True
        return True
    
    def switch_to_next_camera(self):
        """Internal method to switch to next camera"""
        if len(self.available_cameras) <= 1:
            return False
        
        # Release current camera
        if self.cap and self.cap.isOpened():
            self.cap.release()
        
        # Get next camera index
        try:
            current_position = self.available_cameras.index(self.camera_index)
            next_position = (current_position + 1) % len(self.available_cameras)
            self.camera_index = self.available_cameras[next_position]
        except ValueError:
            # Current camera not in list, use first available
            self.camera_index = self.available_cameras[0]
        
        print(f"Switching to camera {self.camera_index}")
        return True

    def stop(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
