import cv2
import numpy as np
from ultralytics import YOLO
import time
from vision.iphone import initialize_camera, switch_camera, get_available_cameras

class PeopleCounter:
    def __init__(self, model_path='best.pt', confidence_threshold=0.5):
        """
        Initialize the people counter with YOLO model
        
        Args:
            model_path: Path to YOLO model file (default: yolov8n.pt)
            confidence_threshold: Minimum confidence for person detection
        """
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.current_count = 0
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.fps = 0
        
        # Colors for bounding boxes (BGR format)
        self.colors = [
            (0, 255, 0),    # Green
            (255, 0, 0),    # Blue
            (0, 0, 255),    # Red
            (255, 255, 0),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Yellow
        ]
    
    def calculate_fps(self):
        """Calculate and update FPS"""
        self.fps_counter += 1
        if self.fps_counter % 30 == 0:  # Update FPS every 30 frames
            current_time = time.time()
            self.fps = 30 / (current_time - self.fps_start_time)
            self.fps_start_time = current_time
    
    def count_persons(self, detections):
        """Count persons in current frame"""
        person_count = 0
        
        for detection in detections:
            if detection.conf > self.confidence_threshold and detection.cls == 0:  # Class 0 is person
                person_count += 1
        
        self.current_count = person_count
        return person_count
    
    def detect_and_count(self, frame, current_camera=None, available_cameras=None):
        """Detect people in frame and return annotated frame"""
        # Run YOLO detection
        results = self.model(frame, verbose=False)
        
        # Get detections
        detections = results[0].boxes if len(results) > 0 and results[0].boxes is not None else []
        
        # Count persons
        person_count = self.count_persons(detections)
        
        # Draw bounding boxes and labels
        for i, detection in enumerate(detections):
            if detection.conf > self.confidence_threshold and detection.cls == 0:
                x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy().astype(int)
                confidence = detection.conf.cpu().numpy()
                
                # Choose color based on detection index
                color = self.colors[i % len(self.colors)]
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                confidence_value = float(confidence.item()) if hasattr(confidence, 'item') else float(confidence)
                label = f"Person: {confidence_value:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Calculate FPS
        self.calculate_fps()
        
        return frame

