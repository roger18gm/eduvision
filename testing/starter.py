import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vision.yolo_people_counter import PeopleCounter
from vision.iphone import get_available_cameras, switch_camera, initialize_camera
import cv2

def main():
    """Main function to run the people counter"""
    print("Press 'q' to quit, 'r' to reset counter, 'c' to change camera")
    
    # Get all available cameras
    available_cameras = get_available_cameras()
    if not available_cameras:
        print("No cameras found!")
        return
    
    print(f"Found {len(available_cameras)} cameras: {', '.join(map(str, available_cameras))}")
    
    # Initialize the people counter
    counter = PeopleCounter()
    
    # Initialize camera automatically (uses first available)
    cap = initialize_camera()
    if cap is None:
        print("Error: Cannot initialize camera.")
        return
    
    # Get current camera index (first available)
    current_camera_index = available_cameras[0]
    
    print("Camera initialized successfully!")
    print("People detection and counting started...")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read from camera.")
                break
            
            # Detect and count people
            annotated_frame = counter.detect_and_count(frame, current_camera_index, available_cameras)
            
            # Display the frame
            cv2.imshow("EduVision - People Counter", annotated_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                counter.current_count = 0
                print("Counter reset!")
            elif key == ord('c'):
                print("Switching camera...")
                new_cap, new_index = switch_camera(cap, current_camera_index, available_cameras)
                if new_cap is not None:
                    cap = new_cap
                    current_camera_index = new_index
                    print(f"Camera switched successfully to index {new_index}!")
                else:
                    print("Failed to switch camera, keeping current camera.")
    
    except KeyboardInterrupt:
        print("\nStopping people counter...")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("Goodbye!")

if __name__ == "__main__":
    main()
