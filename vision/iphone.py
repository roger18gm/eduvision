import cv2

def detect_available_cameras():
    """
    Detect all available cameras and return their indices.
    
    Returns:
        list of available camera indices
    """
    available_cameras = []
    print("Scanning for available cameras...")
    
    # Check indices 0-5 for available cameras (reduced range to avoid errors)
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                available_cameras.append(i)
                print(f"  📱 Camera found at index {i}")
            cap.release()
        else:
            cap.release()
    
    return available_cameras

def get_available_cameras():
    """
    Get list of available cameras without user interaction.
    
    Returns:
        list of available camera indices
    """
    return detect_available_cameras()


def cycle_camera(current_index, available_cameras):
    """
    Cycle to the next camera in the available cameras list.
    
    Args:
        current_index: Current camera index
        available_cameras: List of available camera indices
    
    Returns:
        int: Next camera index, or current if only one camera
    """
    if len(available_cameras) <= 1:
        return current_index
    
    try:
        current_position = available_cameras.index(current_index)
        next_position = (current_position + 1) % len(available_cameras)
        return available_cameras[next_position]
    except ValueError:
        # Current camera not in list, return first available
        return available_cameras[0]

def initialize_camera(camera_index=None):
    """
    Initialize camera at specified index or automatically use first available camera.
    
    Args:
        camera_index: Specific camera index to use (optional)
    
    Returns:
        cv2.VideoCapture object or None if camera not found
    """
    if camera_index is None:
        # Get available cameras and use the first one
        available_cameras = get_available_cameras()
        if not available_cameras:
            print("No cameras available!")
            return None
        camera_index = available_cameras[0]
        print(f"Using first available camera at index {camera_index}")
    
    print(f"Attempting to connect to camera at index {camera_index}...")
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera at index {camera_index}.")
        return None
    
    # Test if we can actually read from the camera
    ret, frame = cap.read()
    if not ret or frame is None:
        print(f"Error: Camera at index {camera_index} opened but cannot read frames.")
        cap.release()
        return None
    
    # Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print(f"Camera at index {camera_index} connected successfully!")
    return cap

def switch_camera(current_cap=None, current_index=None, available_cameras=None):
    """
    Switch to the next camera in the available cameras list.
    
    Args:
        current_cap: Current VideoCapture object to release (optional)
        current_index: Current camera index (optional)
        available_cameras: List of available camera indices (optional)
    
    Returns:
        tuple: (cv2.VideoCapture object, new_camera_index) or (None, None) if no camera found
    """
    # Release current camera if provided
    if current_cap is not None:
        current_cap.release()
    
    # Get available cameras if not provided
    if available_cameras is None:
        available_cameras = get_available_cameras()
    
    if not available_cameras:
        print("No cameras available!")
        return None, None
    
    # Cycle to next camera
    if current_index is not None:
        next_index = cycle_camera(current_index, available_cameras)
    else:
        next_index = available_cameras[0]
    
    print(f"🔄 Switching to camera at index {next_index}...")
    
    # Initialize new camera
    cap = cv2.VideoCapture(next_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera at index {next_index}.")
        return None, None
    
    # Test if we can actually read from the camera
    ret, frame = cap.read()
    if not ret or frame is None:
        print(f"Error: Camera at index {next_index} opened but cannot read frames.")
        cap.release()
        return None, None
    
    # Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print(f"Camera at index {next_index} connected successfully!")
    return cap, next_index
