import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QImage, QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
import cv2
from frontend.camera_thread import CameraThread
from datetime import datetime


class CameraPage(QWidget):
    def __init__(self, db, back_to_dashboard):
        super().__init__()
        self.db = db
        self.back_to_dashboard = back_to_dashboard
        self.building_id = None
        self.room_id = None
        
        # Set up the camera interface
        self.setup_camera_ui()
        
        # --- State ---
        self.camera_thread = None
        self.camera_running = False
        self.current_count = 0

        # --- Auto-start camera ---
        self.start_camera()
    
    def setup_camera_ui(self):
        """Setup the camera interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Title with glow effect
        title = QLabel("📹 Live Camera Feed")
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #00d4ff;
                background: transparent;
            }
        """)
        
        # Status indicator
        status_label = QLabel("🔴 LIVE")
        status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #f44336;
                background: rgba(244, 67, 54, 0.1);
                border: 1px solid #f44336;
                border-radius: 15px;
                padding: 8px 16px;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        # Location info cards
        location_layout = QHBoxLayout()
        location_layout.setSpacing(20)
        
        # Building info card
        self.building_card = self.create_info_card("Building", "Loading...", "#00d4ff")
        self.room_card = self.create_info_card(" Room", "Loading...", "#4caf50")
        self.capacity_card = self.create_info_card(" Capacity", "Loading...", "#ff9800")
        
        location_layout.addWidget(self.building_card)
        location_layout.addWidget(self.room_card)
        location_layout.addWidget(self.capacity_card)
        
        # Main content area with camera on left, cards on right
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        
        # Left side - Camera feed
        camera_section = self.create_camera_section()
        
        # Right side - All cards
        cards_section = self.create_cards_section()
        
        content_layout.addLayout(camera_section, stretch=2)
        content_layout.addLayout(cards_section, stretch=1)
        
        # Navigation controls
        nav_section = self.create_navigation_section()
        
        # Add all sections to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(content_layout)
        main_layout.addLayout(nav_section)
        
        self.setLayout(main_layout)
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                color: #ffffff;
            }
        """)
    
    def create_info_card(self, title, value, color):
        """Create an info card."""
        card = QFrame()
        card.setFixedHeight(80)
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid {color}40;
                border-radius: 12px;
                padding: 15px;
            }}
            QFrame * {{
                background: transparent;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {color};
                font-weight: 500;
                margin-bottom: 5px;
                background: transparent;
                border: none;
            }}
        """)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
                background: transparent;
                border: none;
            }
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        card.setLayout(layout)
        return card
    
    def create_camera_section(self):
        """Create the camera section."""
        section_layout = QVBoxLayout()
        
        # Video container with styling
        video_container = QFrame()
        video_container.setStyleSheet("""
            QFrame {
                background: rgba(0, 0, 0, 0.8);
                border: 3px solid #00d4ff;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        video_layout = QVBoxLayout()
        video_layout.setContentsMargins(10, 10, 10, 10)
        
        # Video display
        self.video_label = QLabel()
        self.video_label.setMinimumSize(900, 700)
        self.video_label.setScaledContents(True)
        self.video_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border: 2px solid #00d4ff;
                border-radius: 15px;
                color: #ffffff;
                min-width: 900px;
                min-height: 700px;
            }
        """)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setText("Initializing Camera...")
        
        video_layout.addWidget(self.video_label, alignment=Qt.AlignCenter)
        video_container.setLayout(video_layout)
        
        section_layout.addWidget(video_container)
        return section_layout
    
    def create_cards_section(self):
        """Create the cards section with all cards on the right side."""
        section_layout = QVBoxLayout()
        section_layout.setSpacing(20)
        
        # Location cards (Building, Room, Capacity)
        location_cards_layout = QVBoxLayout()
        location_cards_layout.setSpacing(15)
        
        # Building card 
        self.building_card = self.create_info_card("Building", "Loading...", "#00d4ff")
        location_cards_layout.addWidget(self.building_card)
        
        # Room card 
        self.room_card = self.create_info_card("Room", "Loading...", "#4caf50")
        location_cards_layout.addWidget(self.room_card)
        
        # Capacity card
        self.capacity_card = self.create_info_card("Capacity", "Loading...", "#ff9800")
        location_cards_layout.addWidget(self.capacity_card)
        
        section_layout.addLayout(location_cards_layout)
        
        # Analytics cards (People Count, Status)
        analytics_cards_layout = QVBoxLayout()
        analytics_cards_layout.setSpacing(15)
        
        # People count card 
        self.count_card = self.create_analytics_card(" People Count", "0", "#00d4ff")
        analytics_cards_layout.addWidget(self.count_card)
        
        # Status card 
        self.status_card = self.create_analytics_card("Status", "🟢 Active", "#4caf50")
        analytics_cards_layout.addWidget(self.status_card)
        
        section_layout.addLayout(analytics_cards_layout)
        section_layout.addStretch()
        
        return section_layout
    
    def create_info_card(self, title, value, color):
        """Create info card."""
        card = QFrame()
        card.setMinimumHeight(120)
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid {color}40;
                border-radius: 15px;
                padding: 15px;
            }}
            QFrame * {{
                background: transparent;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                color: {color};
                font-weight: 500;
                background: transparent;
                border: none;
                padding: 5px;
            }}
        """)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #ffffff;
                background: transparent;
                border: none;
                padding: 5px;
            }
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        card.setLayout(layout)
        return card
    
    def create_analytics_card(self, title, value, color):
        """Create a analytics card ."""
        card = QFrame()
        card.setMinimumHeight(140)
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid {color}40;
                border-radius: 15px;
                padding: 15px;
            }}
            QFrame * {{
                background: transparent;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                color: {color};
                font-weight: 500;
                background: transparent;
                border: none;
                padding: 5px;
            }}
        """)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: #ffffff;
                background: transparent;
                border: none;
                padding: 5px;
            }}
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        card.setLayout(layout)
        
        # Store reference to value label for updates
        card.value_label = value_label
        return card
    
    def create_navigation_section(self):
        """Create the navigation section."""
        section_layout = QHBoxLayout()
        section_layout.setSpacing(15)
        
        # Back button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #757575, stop:1 #616161);
                border: none;
                border-radius: 10px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9e9e9e, stop:1 #757575);
            }
        """)
        back_btn.clicked.connect(self.back_to_dashboard)
        
        # Camera controls
        prev_btn = QPushButton("Previous")
        prev_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff9800, stop:1 #f57c00);
                border: none;
                border-radius: 10px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffb74d, stop:1 #ff9800);
            }
        """)
        prev_btn.clicked.connect(self.switch_camera)
        
        next_btn = QPushButton("Next")
        next_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff9800, stop:1 #f57c00);
                border: none;
                border-radius: 10px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffb74d, stop:1 #ff9800);
            }
        """)
        next_btn.clicked.connect(self.switch_camera)
        
        # Snapshot button
        snapshot_btn = QPushButton("Take Snapshot")
        snapshot_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4caf50, stop:1 #388e3c);
                border: none;
                border-radius: 10px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #66bb6a, stop:1 #4caf50);
            }
        """)
        snapshot_btn.clicked.connect(self.take_snapshot)
        
        section_layout.addWidget(back_btn)
        section_layout.addStretch()
        section_layout.addWidget(prev_btn)
        section_layout.addWidget(next_btn)
        section_layout.addWidget(snapshot_btn)
        
        return section_layout

    # ---------------------
    # CAMERA CONTROL
    # ---------------------

    def start_camera(self):
        self.camera_thread = CameraThread()
        self.camera_thread.frame_ready.connect(self.update_frame)
        self.camera_thread.people_count.connect(self.update_count)
        self.camera_thread.start()

        self.camera_running = True

    def stop_camera(self):
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_thread.wait()
            self.camera_thread = None

        self.video_label.clear()
        self.count_label.setText("People in the room: 0")
        self.camera_running = False

    # ---------------------
    # FRAME UPDATES
    # ---------------------
    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_image = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def update_count(self, count):
        if hasattr(self, 'count_card'):
            self.count_card.value_label.setText(str(count))
        self.current_count = count

    def switch_camera(self):
        """Switch to the next available camera"""
        if self.camera_thread and self.camera_running:
            success = self.camera_thread.switch_camera()
            if success:
                print("Camera switch requested successfully")
            else:
                print("No other cameras available or switch failed")
        else:
            print("Camera is not running")

    def take_snapshot(self):
        """Take a snapshot of current count and timestamp"""
        if self.camera_running:
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            print(f"📸 Snapshot taken:")
            print(f"   Current Room Id: {self.room_id}")
            print(f"   People in room: {self.current_count}")
            print(f"   Timestamp: {timestamp}")

            # TODO: Save to database
            self.db.save_snapshot(self.room_id, timestamp, self.current_count)

        else:
            print("Camera is not running - cannot take snapshot")

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

    def set_location(self, building_id, room_id):
        self.building_id = building_id
        self.room_id = room_id
        print(
            f"CameraPage location set to Building ID: {building_id}, Room ID: {room_id}")
        room = self.db.get_room(room_id)
        building = self.db.get_building(building_id)
        print("Building from DB:", building)
        print("Room from DB:", room)

        # Update the info cards
        if hasattr(self, 'building_card'):
            # Update building card
            building_layout = self.building_card.layout()
            if building_layout and building_layout.count() > 1:
                building_layout.itemAt(1).widget().setText(building['name'])
        
        if hasattr(self, 'room_card'):
            # Update room card
            room_layout = self.room_card.layout()
            if room_layout and room_layout.count() > 1:
                room_layout.itemAt(1).widget().setText(room['number'])
        
        if hasattr(self, 'capacity_card'):
            # Update capacity card
            capacity_layout = self.capacity_card.layout()
            if capacity_layout and capacity_layout.count() > 1:
                capacity_layout.itemAt(1).widget().setText(str(room['capacity']))
