import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DashboardPage(QWidget):
    def __init__(self, switch_to_camera):
        super().__init__()

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
        buildingComboBox = QComboBox()
        buildingComboBox.addItems(["Building A", "Building B", "Building C"])
        buildingComboBox.setStyleSheet("font-size: 16px; padding: 6px;")
        roomComboBox = QComboBox()
        roomComboBox.addItems(["Room 101", "Room 102", "Room 201"])
        roomComboBox.setStyleSheet("font-size: 16px; padding: 6px;")
        automation_btn = QPushButton("Go to Automation")
        automation_btn.setStyleSheet(
            "background-color: #43a047; color: white; font-size: 16px; padding: 8px; margin-top: 16px;")
        automation_btn.clicked.connect(self.switch_to_automation)
        camera_btn = QPushButton("Go to Camera")
        camera_btn.setStyleSheet(
            "background-color: #1976d2; color: white; font-size: 16px; padding: 8px; margin-top: 8px;")
        camera_btn.clicked.connect(switch_to_camera)

        controls_container.addWidget(title)
        controls_container.addWidget(buildingComboBox)
        controls_container.addWidget(roomComboBox)
        controls_container.addWidget(automation_btn)
        controls_container.addWidget(camera_btn)
        controls_container.addStretch()

        # --- Add to Main Layout ---
        main_layout.addLayout(graph_container, stretch=2)
        main_layout.addLayout(controls_container, stretch=1)

        self.setLayout(main_layout)
        self.setStyleSheet("background: #f5f5f5;")

        self.plot_sample_graph()

    def plot_sample_graph(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot([1, 2, 3, 4], [10, 20, 15, 25], marker='o')
        ax.set_title("Sample Attendance Graph")
        ax.set_xlabel("Day")
        ax.set_ylabel("Count")
        self.canvas.draw()

    def switch_to_automation(self):
        pass  # Placeholder for automation page switch
