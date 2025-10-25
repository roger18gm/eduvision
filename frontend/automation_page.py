import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QComboBox, QSpinBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QGroupBox, QFormLayout)
import PyQt5.QtCore as QtCore
from datetime import datetime
from automation.automation_scheduler import AutomationScheduler


class AutomationPage(QWidget):
    def __init__(self, back_to_dashboard, snapshot_callback):
        super().__init__()
        self.back_to_dashboard = back_to_dashboard
        self.snapshot_callback = snapshot_callback
        self.scheduler = AutomationScheduler(snapshot_callback)
        
        # Start the scheduler
        self.scheduler.start_scheduler()
        
        self.setup_ui()
        self.refresh_schedules_table()
    
    def setup_ui(self):
        """Setup the automation page UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Automation Scheduler")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
        # Create main content layout
        main_layout = QHBoxLayout()
        
        # Left side - Schedule creation
        left_panel = self.create_schedule_panel()
        
        # Right side - Active schedules
        right_panel = self.create_schedules_panel()
        
        main_layout.addLayout(left_panel, stretch=1)
        main_layout.addLayout(right_panel, stretch=2)
        
        # Navigation
        nav_layout = QHBoxLayout()
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet(
            "background-color: #757575; color: white; font-size: 15px; padding: 8px 18px; border-radius: 6px;"
        )
        back_btn.clicked.connect(self.back_to_dashboard)
        
        nav_layout.addWidget(back_btn)
        nav_layout.addStretch()
        
        # Add to main layout
        layout.addWidget(title)
        layout.addLayout(main_layout)
        layout.addLayout(nav_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background: #f5f5f5;")
    
    def create_schedule_panel(self):
        """Create the schedule creation panel."""
        panel_layout = QVBoxLayout()
        
        # Schedule creation group
        creation_group = QGroupBox("Create New Schedule")
        creation_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        creation_layout = QFormLayout()
        
        # Schedule type
        self.schedule_type = QComboBox()
        self.schedule_type.addItems(["Hourly", "Daily", "Weekly", "Custom Interval"])
        self.schedule_type.currentTextChanged.connect(self.on_schedule_type_changed)
        creation_layout.addRow("Schedule Type:", self.schedule_type)
        
        # Schedule name
        self.schedule_name = QLabel("Schedule Name:")
        self.schedule_name_input = QLabel()  # Will be replaced with QLineEdit
        creation_layout.addRow(self.schedule_name, self.schedule_name_input)
        
        # Time controls (will be shown/hidden based on type)
        self.time_controls = QWidget()
        self.time_layout = QFormLayout()
        self.time_controls.setLayout(self.time_layout)
        
        # Hour control
        self.hour_spin = QSpinBox()
        self.hour_spin.setRange(0, 23)
        self.hour_spin.setValue(9)
        self.hour_label = QLabel("Hour:")
        self.time_layout.addRow(self.hour_label, self.hour_spin)
        
        # Minute control
        self.minute_spin = QSpinBox()
        self.minute_spin.setRange(0, 59)
        self.minute_spin.setValue(0)
        self.minute_label = QLabel("Minute:")
        self.time_layout.addRow(self.minute_label, self.minute_spin)
        
        # Day of week control
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.day_label = QLabel("Day of Week:")
        self.time_layout.addRow(self.day_label, self.day_combo)
        
        # Interval control
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 1440)  # 1 minute to 24 hours
        self.interval_spin.setValue(30)
        self.interval_label = QLabel("Interval (minutes):")
        self.time_layout.addRow(self.interval_label, self.interval_spin)
        
        creation_layout.addRow(self.time_controls)
        
        # Create button
        create_btn = QPushButton("Create Schedule")
        create_btn.setStyleSheet(
            "background-color: #4caf50; color: white; font-size: 16px; padding: 10px; border-radius: 6px;"
        )
        create_btn.clicked.connect(self.create_schedule)
        creation_layout.addRow(create_btn)
        
        creation_group.setLayout(creation_layout)
        panel_layout.addWidget(creation_group)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        actions_layout = QVBoxLayout()
        
        # Quick schedule buttons
        hourly_btn = QPushButton("Every Hour")
        hourly_btn.setStyleSheet("background-color: #2196f3; color: white; padding: 8px;")
        hourly_btn.clicked.connect(lambda: self.create_quick_schedule("hourly"))
        
        daily_btn = QPushButton("Daily at 9 AM")
        daily_btn.setStyleSheet("background-color: #ff9800; color: white; padding: 8px;")
        daily_btn.clicked.connect(lambda: self.create_quick_schedule("daily"))
        
        weekly_btn = QPushButton("Weekly (Monday 9 AM)")
        weekly_btn.setStyleSheet("background-color: #9c27b0; color: white; padding: 8px;")
        weekly_btn.clicked.connect(lambda: self.create_quick_schedule("weekly"))
        
        actions_layout.addWidget(hourly_btn)
        actions_layout.addWidget(daily_btn)
        actions_layout.addWidget(weekly_btn)
        
        actions_group.setLayout(actions_layout)
        panel_layout.addWidget(actions_group)
        
        panel_layout.addStretch()
        return panel_layout
    
    def create_schedules_panel(self):
        """Create the active schedules panel."""
        panel_layout = QVBoxLayout()
        
        # Active schedules group
        schedules_group = QGroupBox("Active Schedules")
        schedules_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        schedules_layout = QVBoxLayout()
        
        # Schedules table
        self.schedules_table = QTableWidget()
        self.schedules_table.setColumnCount(5)
        self.schedules_table.setHorizontalHeaderLabels([
            "Schedule ID", "Type", "Schedule", "Next Run", "Actions"
        ])
        
        # Set table properties
        header = self.schedules_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.schedules_table.setAlternatingRowColors(True)
        self.schedules_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        schedules_layout.addWidget(self.schedules_table)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("background-color: #607d8b; color: white; padding: 8px;")
        refresh_btn.clicked.connect(self.refresh_schedules_table)
        
        clear_all_btn = QPushButton("Clear All")
        clear_all_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        clear_all_btn.clicked.connect(self.clear_all_schedules)
        
        control_layout.addWidget(refresh_btn)
        control_layout.addWidget(clear_all_btn)
        control_layout.addStretch()
        
        schedules_layout.addLayout(control_layout)
        schedules_group.setLayout(schedules_layout)
        panel_layout.addWidget(schedules_group)
        
        return panel_layout
    
    def on_schedule_type_changed(self, schedule_type):
        """Handle schedule type change."""
        # Show/hide relevant controls
        if schedule_type == "Hourly":
            self.hour_label.hide()
            self.hour_spin.hide()
            self.day_label.hide()
            self.day_combo.hide()
            self.interval_label.hide()
            self.interval_spin.hide()
            self.minute_label.show()
            self.minute_spin.show()
        elif schedule_type == "Daily":
            self.day_label.hide()
            self.day_combo.hide()
            self.interval_label.hide()
            self.interval_spin.hide()
            self.hour_label.show()
            self.hour_spin.show()
            self.minute_label.show()
            self.minute_spin.show()
        elif schedule_type == "Weekly":
            self.interval_label.hide()
            self.interval_spin.hide()
            self.hour_label.show()
            self.hour_spin.show()
            self.minute_label.show()
            self.minute_spin.show()
            self.day_label.show()
            self.day_combo.show()
        elif schedule_type == "Custom Interval":
            self.hour_label.hide()
            self.hour_spin.hide()
            self.minute_label.hide()
            self.minute_spin.hide()
            self.day_label.hide()
            self.day_combo.hide()
            self.interval_label.show()
            self.interval_spin.show()
    
    def create_schedule(self):
        """Create a new schedule based on current settings."""
        schedule_type = self.schedule_type.currentText()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if schedule_type == "Hourly":
            schedule_id = f"hourly_{timestamp}"
            minute = self.minute_spin.value()
            self.scheduler.add_hourly_schedule(schedule_id, minute)
            
        elif schedule_type == "Daily":
            schedule_id = f"daily_{timestamp}"
            hour = self.hour_spin.value()
            minute = self.minute_spin.value()
            self.scheduler.add_daily_schedule(schedule_id, hour, minute)
            
        elif schedule_type == "Weekly":
            schedule_id = f"weekly_{timestamp}"
            day_of_week = self.day_combo.currentText().lower()
            hour = self.hour_spin.value()
            minute = self.minute_spin.value()
            self.scheduler.add_weekly_schedule(schedule_id, day_of_week, hour, minute)
            
        elif schedule_type == "Custom Interval":
            schedule_id = f"interval_{timestamp}"
            minutes = self.interval_spin.value()
            self.scheduler.add_custom_interval(schedule_id, minutes)
        
        self.refresh_schedules_table()
        QMessageBox.information(self, "Success", f"Schedule '{schedule_id}' created successfully!")
    
    def create_quick_schedule(self, schedule_type):
        """Create a quick schedule."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if schedule_type == "hourly":
            schedule_id = f"quick_hourly_{timestamp}"
            self.scheduler.add_hourly_schedule(schedule_id, 0)
            
        elif schedule_type == "daily":
            schedule_id = f"quick_daily_{timestamp}"
            self.scheduler.add_daily_schedule(schedule_id, 9, 0)
            
        elif schedule_type == "weekly":
            schedule_id = f"quick_weekly_{timestamp}"
            self.scheduler.add_weekly_schedule(schedule_id, "monday", 9, 0)
        
        self.refresh_schedules_table()
        QMessageBox.information(self, "Success", f"Quick schedule '{schedule_id}' created!")
    
    def refresh_schedules_table(self):
        """Refresh the schedules table."""
        schedules = self.scheduler.get_all_schedules()
        next_runs = self.scheduler.get_next_run_times()
        
        self.schedules_table.setRowCount(len(schedules))
        
        for row, (schedule_id, schedule_data) in enumerate(schedules.items()):
            # Schedule ID
            self.schedules_table.setItem(row, 0, QTableWidgetItem(schedule_id))
            
            # Type
            self.schedules_table.setItem(row, 1, QTableWidgetItem(schedule_data['type'].title()))
            
            # Schedule description
            if schedule_data['type'] == 'hourly':
                desc = f"Every hour at minute {schedule_data['minute']}"
            elif schedule_data['type'] == 'daily':
                desc = f"Daily at {schedule_data['hour']:02d}:{schedule_data['minute']:02d}"
            elif schedule_data['type'] == 'weekly':
                desc = f"Weekly on {schedule_data['day_of_week']} at {schedule_data['hour']:02d}:{schedule_data['minute']:02d}"
            elif schedule_data['type'] == 'interval':
                desc = f"Every {schedule_data['minutes']} minutes"
            else:
                desc = "Unknown"
            
            self.schedules_table.setItem(row, 2, QTableWidgetItem(desc))
            
            # Next run
            next_run = next_runs.get(schedule_id, "Unknown")
            self.schedules_table.setItem(row, 3, QTableWidgetItem(next_run))
            
            # Actions
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 4px;")
            delete_btn.clicked.connect(lambda checked, sid=schedule_id: self.delete_schedule(sid))
            self.schedules_table.setCellWidget(row, 4, delete_btn)
    
    def delete_schedule(self, schedule_id):
        """Delete a schedule."""
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Are you sure you want to delete schedule '{schedule_id}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.scheduler.remove_schedule(schedule_id)
            self.refresh_schedules_table()
            QMessageBox.information(self, "Success", f"Schedule '{schedule_id}' deleted!")
    
    def clear_all_schedules(self):
        """Clear all schedules."""
        reply = QMessageBox.question(self, "Confirm Clear All", 
                                   "Are you sure you want to clear ALL schedules?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.scheduler.clear_all_schedules()
            self.refresh_schedules_table()
            QMessageBox.information(self, "Success", "All schedules cleared!")
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.scheduler.stop_scheduler()
        event.accept()
