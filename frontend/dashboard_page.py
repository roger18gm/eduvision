import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DashboardPage(QWidget):
    def __init__(self, db, switch_to_camera, switch_to_automation):
        super().__init__()
        self.db = db
        self.switch_to_camera = switch_to_camera
        self.switch_to_automation = switch_to_automation

        # --- Main Layout ---
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)

        # --- Left: Matplotlib Graph ---
        graph_container = QVBoxLayout()
        graph_title = QLabel("Attendance Graph")
        graph_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; margin-bottom: 16px;")
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        graph_container.addWidget(graph_title)
        graph_container.addWidget(self.canvas)
        graph_container.addStretch()

        # --- Right: Controls ---
        controls_container = QVBoxLayout()
        title = QLabel("Dashboard Page")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 24px;")

        self.buildingComboBox = QComboBox()
        self.buildingComboBox.addItems(
            ["Building A", "Building B", "Building C"])
        self.buildingComboBox.setStyleSheet("font-size: 16px; padding: 6px;")
        self.buildingComboBox.currentIndexChanged.connect(
            self.on_building_changed)

        self.roomComboBox = QComboBox()
        self.roomComboBox.addItems(["Room 101", "Room 102", "Room 201"])
        self.roomComboBox.setStyleSheet("font-size: 16px; padding: 6px;")

        automation_btn = QPushButton("Go to Automation")
        automation_btn.setStyleSheet(
            "background-color: #43a047; color: white; font-size: 16px; padding: 8px; margin-top: 16px;")
        automation_btn.clicked.connect(self.go_to_automation)

        camera_btn = QPushButton("Go to Camera")
        camera_btn.setStyleSheet(
            "background-color: #1976d2; color: white; font-size: 16px; padding: 8px; margin-top: 8px;")
        camera_btn.clicked.connect(switch_to_camera)

        controls_container.addWidget(title)
        controls_container.addWidget(self.buildingComboBox)
        controls_container.addWidget(self.roomComboBox)
        controls_container.addWidget(automation_btn)
        controls_container.addWidget(camera_btn)
        controls_container.addStretch()

        # --- Add to Main Layout ---
        main_layout.addLayout(graph_container, stretch=2)
        main_layout.addLayout(controls_container, stretch=1)

        self.setLayout(main_layout)
        self.setStyleSheet("background: #f5f5f5;")

        self.plot_sample_graph()
        self.load_buildings()

    def plot_sample_graph(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot([1, 2, 3, 4], [10, 20, 15, 25], marker='o')
        ax.set_title("Sample Attendance Graph")
        ax.set_xlabel("Day")
        ax.set_ylabel("Count")
        self.canvas.draw()

    def go_to_automation(self):
        self.switch_to_automation()

    def load_buildings(self):
        buildings = self.db.get_buildings()
        self.buildingComboBox.clear()
        self.building_ids = []
        for b in buildings:
            self.buildingComboBox.addItem(b['name'])
            self.building_ids.append(b['building_id'])
        if buildings:
            self.load_rooms(self.building_ids[0])

    def on_building_changed(self, index):
        if index >= 0 and index < len(self.building_ids):
            building_id = self.building_ids[index]
            self.load_rooms(building_id)

    def load_rooms(self, building_id):
        rooms = self.db.get_rooms_by_building(building_id)
        self.roomComboBox.clear()
        for r in rooms:
            self.roomComboBox.addItem(r['number'])
