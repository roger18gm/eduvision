import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QGridLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class DashboardPage(QWidget):
    def __init__(self, db, switch_to_camera, switch_to_automation):
        super().__init__()
        self.db = db
        self.switch_to_camera = switch_to_camera
        self.switch_to_automation = switch_to_automation
        self.selected_building_id = None
        self.selected_room_id = None

        # Set up the futuristic dashboard layout
        self.setup_dashboard_ui()
        
        # Configure matplotlib for dark theme
        self.setup_matplotlib_theme()
        
        self.buildingComboBox.currentIndexChanged.connect(self.on_building_changed)
        self.roomComboBox.currentIndexChanged.connect(self.on_room_changed)

        self.plot_sample_graph()
        self.load_buildings()
    
    def setup_dashboard_ui(self):
        """Setup the futuristic dashboard UI."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Title with glow effect
        title = QLabel("EduVision Dashboard")
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #00d4ff;
                background: transparent;
            }
        """)
        
        # Status indicator
        status_label = QLabel("🟢 System Online")
        status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #4caf50;
                background: rgba(76, 175, 80, 0.1);
                border: 1px solid #4caf50;
                border-radius: 15px;
                padding: 8px 16px;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        # Main content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        
        # Left side - Analytics cards and chart
        left_panel = self.create_analytics_panel()
        
        # Right side - Controls and navigation
        right_panel = self.create_controls_panel()
        
        content_layout.addLayout(left_panel, stretch=2)
        content_layout.addLayout(right_panel, stretch=1)
        
        # Add to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(content_layout)
        
        self.setLayout(main_layout)
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                color: #ffffff;
            }
        """)
    
    def create_analytics_panel(self):
        """Create the analytics panel with cards and chart."""
        panel_layout = QVBoxLayout()
        panel_layout.setSpacing(20)
        
        # Analytics cards
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)
        cards_layout.setContentsMargins(5, 5, 5, 5)
        
        # Card 1: Total Attendance
        card1 = self.create_metric_card("Total Attendance", "1,247", "+12%", "#00d4ff")
        cards_layout.addWidget(card1, 0, 0)
        
        # Card 2: Active Rooms
        card2 = self.create_metric_card("Active Rooms", "24", "+3", "#4caf50")
        cards_layout.addWidget(card2, 0, 1)
        
        # Card 3: Peak Hours
        card3 = self.create_metric_card("Peak Hours", "2:00 PM", "Today", "#ff9800")
        cards_layout.addWidget(card3, 1, 0)
        
        # Card 4: Efficiency
        card4 = self.create_metric_card("Efficiency", "94%", "+2%", "#9c27b0")
        cards_layout.addWidget(card4, 1, 1)
        
        panel_layout.addLayout(cards_layout)
        
        # Chart section - bigger
        chart_frame = QFrame()
        chart_frame.setMinimumHeight(500)
        chart_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(0, 212, 255, 0.3);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        
        chart_layout = QVBoxLayout()
        chart_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create matplotlib figure with dark theme - bigger size
        self.figure = Figure(figsize=(10, 7), facecolor='#1a1a2e')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: transparent;")
        
        chart_layout.addWidget(self.canvas)
        chart_frame.setLayout(chart_layout)
        
        panel_layout.addWidget(chart_frame)
        return panel_layout
    
    def create_metric_card(self, title, value, change, color):
        """Create a metric card with futuristic styling - fixed size."""
        card = QFrame()
        card.setFixedSize(200, 140)
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid {color}40;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
            }}
            QFrame:hover {{
                border: 2px solid {color};
            }}
            QFrame * {{
                background: transparent;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(3)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {color};
                font-weight: 500;
                background: transparent;
                border: none;
                padding: 1px;
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
                padding: 1px;
            }
        """)
        
        # Change indicator
        change_label = QLabel(change)
        change_label.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                color: {color};
                font-weight: 500;
                background: transparent;
                border: none;
                padding: 1px;
            }}
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(change_label)
        layout.addStretch()
        
        card.setLayout(layout)
        return card
    
    def create_controls_panel(self):
        """Create the controls panel."""
        panel_layout = QVBoxLayout()
        panel_layout.setSpacing(20)
        
        # Controls frame
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(0, 212, 255, 0.3);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(20)
        
        # Title
        title = QLabel("🎛️ System Controls")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #00d4ff;
                margin-bottom: 20px;
            }
        """)
        
        # Building selection
        building_label = QLabel("Select Building")
        building_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #ffffff;
                font-weight: 500;
                margin-bottom: 8px;
            }
        """)
        
        self.buildingComboBox = QComboBox()
        self.buildingComboBox.addItems(["Building A", "Building B", "Building C"])
        self.buildingComboBox.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(0, 212, 255, 0.3);
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                padding: 10px;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #00d4ff;
            }
        """)
        
        # Room selection
        room_label = QLabel("Select Room")
        room_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #ffffff;
                font-weight: 500;
                margin-bottom: 8px;
            }
        """)
        
        self.roomComboBox = QComboBox()
        self.roomComboBox.addItems(["Room 101", "Room 102", "Room 201"])
        self.roomComboBox.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(0, 212, 255, 0.3);
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                padding: 10px;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #00d4ff;
            }
        """)
        
        # Action buttons
        camera_btn = QPushButton("Live Camera")
        camera_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00d4ff, stop:1 #0099cc);
                border: none;
                border-radius: 10px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00e5ff, stop:1 #00b3e6);
            }
        """)
        camera_btn.clicked.connect(self.switch_to_camera)
        
        automation_btn = QPushButton("Automation")
        automation_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4caf50, stop:1 #388e3c);
                border: none;
                border-radius: 10px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #66bb6a, stop:1 #4caf50);
            }
        """)
        automation_btn.clicked.connect(self.go_to_automation)
        
        # Add all widgets
        controls_layout.addWidget(title)
        controls_layout.addWidget(building_label)
        controls_layout.addWidget(self.buildingComboBox)
        controls_layout.addWidget(room_label)
        controls_layout.addWidget(self.roomComboBox)
        controls_layout.addWidget(camera_btn)
        controls_layout.addWidget(automation_btn)
        controls_layout.addStretch()
        
        controls_frame.setLayout(controls_layout)
        panel_layout.addWidget(controls_frame)
        
        return panel_layout
    
    def setup_matplotlib_theme(self):
        """Setup matplotlib for dark theme."""
        plt.style.use('dark_background')
        # Set seaborn style for dark theme
        sns.set_style("darkgrid")
        sns.set_palette("husl")

    def plot_sample_graph(self, data=None, title="Real-time Analytics"):
        # Clear the figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Set dark theme colors
        ax.set_facecolor('#1a1a2e')
        ax.tick_params(colors='#ffffff')
        ax.spines['bottom'].set_color('#00d4ff')
        ax.spines['top'].set_color('#00d4ff')
        ax.spines['right'].set_color('#00d4ff')
        ax.spines['left'].set_color('#00d4ff')
        
        if data is not None:
            # Example: data should be a pandas DataFrame
            sns.barplot(data=data, x="date", y="attendance", ax=ax, color='#00d4ff')
            ax.set_title(title, color='#00d4ff', fontsize=16, fontweight='bold')
            ax.set_xlabel("Date", color='#ffffff')
            ax.set_ylabel("Attendance", color='#ffffff')
        else:
            # Create a more futuristic sample plot
            x = np.linspace(0, 24, 100)
            y = 50 + 30 * np.sin(x * np.pi / 12) + 10 * np.random.random(100)
            
            # Create gradient line
            ax.plot(x, y, color='#00d4ff', linewidth=3, alpha=0.8)
            ax.fill_between(x, y, alpha=0.3, color='#00d4ff')
            
            # Add some futuristic styling
            ax.set_title(title, color='#00d4ff', fontsize=16, fontweight='bold')
            ax.set_xlabel("Time (Hours)", color='#ffffff')
            ax.set_ylabel("People Count", color='#ffffff')
            ax.grid(True, alpha=0.3, color='#00d4ff')
            
            # Add glow effect simulation with multiple lines
            for i in range(3):
                ax.plot(x, y, color='#00d4ff', linewidth=1, alpha=0.1)
        
        self.canvas.draw()

    def go_to_automation(self):
        self.switch_to_automation()

    def on_building_changed(self, index):
        if index >= 0 and index < len(self.building_ids):
            self.selected_building_id = self.building_ids[index]
            self.load_rooms(self.selected_building_id)
            self.update_plot_for_building(self.selected_building_id)

    def on_room_changed(self, index):
        if hasattr(self, 'room_ids') and index >= 0 and index < len(self.room_ids):
            self.selected_room_id = self.room_ids[index]
            self.update_plot_for_room(self.selected_room_id)

    def load_rooms(self, building_id):
        rooms = self.db.get_rooms_by_building(building_id)
        self.roomComboBox.clear()
        self.room_ids = []
        for r in rooms:
            self.roomComboBox.addItem(r['number'])
            self.room_ids.append(r['room_id'])

        if rooms:
            # Set initial room
            self.selected_room_id = self.room_ids[0]

    def update_plot_for_building(self, building_id):
        # Fetch attendance or other data for the building
        # Example: Replace with your actual query
        import pandas as pd
        # Dummy data for demonstration
        data = pd.DataFrame({
            "date": ["2023-10-01", "2023-10-02", "2023-10-03"],
            "attendance": [20, 25, 22]
        })
        self.plot_sample_graph(
            data, title=f"Attendance for Building {building_id}")

    def update_plot_for_room(self, room_id):
        # Fetch attendance or other data for the room
        import pandas as pd
        # Dummy data for demonstration
        data = pd.DataFrame({
            "date": ["2023-10-01", "2023-10-02", "2023-10-03"],
            "attendance": [12, 15, 14]
        })
        self.plot_sample_graph(data, title=f"Attendance for Room {room_id}")

    def load_buildings(self):
        buildings = self.db.get_buildings()
        self.buildingComboBox.clear()
        self.building_ids = []
        for b in buildings:
            self.buildingComboBox.addItem(b['name'])
            self.building_ids.append(b['building_id'])
        if buildings:
            # Set initial building
            self.selected_building_id = self.building_ids[0]
            self.load_rooms(self.building_ids[0])
