#!/usr/bin/env python3
"""
Simple camera comparison - just run both models on camera index 1
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time

def main():
    # Load models
    print("Loading models...")
    original_model = YOLO('yolov8n.pt')
    
    if not os.path.exists('best.pt'):
        print("best.pt not found!")
        return
    
    finetuned_model = YOLO('best.pt')
    print("Both models loaded!")
    
    # Open camera
    cap = cv2.VideoCapture(1)  # Camera index 1
    if not cap.isOpened():
        print("Could not open camera 1")
        return
    
    # Set camera resolution to higher quality
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("Camera opened. Press 'q' to quit, 's' to switch models")
    
    current_model = "original"
    confidence_threshold = 0.5
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Choose model
        if current_model == "original":
            model = original_model
            model_name = "Original"
        else:
            model = finetuned_model
            model_name = "Fine-tuned"
        
        # Run detection
        results = model(frame, verbose=False)
        detections = results[0].boxes if len(results) > 0 and results[0].boxes is not None else []
        
        # Count people
        person_count = 0
        for detection in detections:
            if detection.conf > confidence_threshold:
                class_id = int(detection.cls)
                class_name = model.names[class_id]
                if class_name == 'person':
                    person_count += 1
        
        # Draw bounding boxes
        annotated_frame = frame.copy()
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        
        for i, detection in enumerate(detections):
            if detection.conf > confidence_threshold:
                x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy().astype(int)
                confidence = detection.conf.cpu().numpy()
                class_id = int(detection.cls)
                class_name = model.names[class_id]
                
                color = colors[i % len(colors)]
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                confidence_value = float(confidence.item()) if hasattr(confidence, 'item') else float(confidence)
                label = f"{class_name}: {confidence_value:.2f}"
                cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Add info text
        cv2.putText(annotated_frame, f"Model: {model_name}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(annotated_frame, f"People: {person_count}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(annotated_frame, "Press 's' to switch models", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show frame in full screen size
        cv2.namedWindow('Model Comparison', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Model Comparison', 1280, 720)
        cv2.imshow('Model Comparison', annotated_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            current_model = "finetuned" if current_model == "original" else "original"
            print(f"Switched to {current_model} model")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import os
    main()
