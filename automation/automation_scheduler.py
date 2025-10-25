import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Callable, Optional, Dict, Any
import json
import os


class AutomationScheduler:
    """
    Handles automated snapshot scheduling for the EduVision system.
    Supports various scheduling patterns: hourly, daily, weekly, custom intervals.
    """
    
    def __init__(self, snapshot_callback: Callable[[], Dict[str, Any]]):
        """
        Initialize the automation scheduler.
        
        Args:
            snapshot_callback: Function to call when taking a snapshot.
                               Should return a dictionary with snapshot data.
        """
        self.snapshot_callback = snapshot_callback
        self.scheduler_thread = None
        self.running = False
        self.schedules = {}  # Store active schedules
        self.schedule_file = "automation/schedules.json"
        
        # Create automation directory if it doesn't exist
        os.makedirs("automation", exist_ok=True)
        
        # Load existing schedules
        self.load_schedules()
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread."""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            print("Automation scheduler started")
    
    def stop_scheduler(self):
        """Stop the scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        print("Automation scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(1)  # Check every second
    
    def add_hourly_schedule(self, schedule_id: str, minute: int = 0):
        """
        Add an hourly schedule.
        
        Args:
            schedule_id: Unique identifier for this schedule
            minute: Minute of the hour to trigger (0-59)
        """
        job = schedule.every().hour.at(f"{minute:02d}:00").do(self._take_scheduled_snapshot, schedule_id)
        self.schedules[schedule_id] = {
            'type': 'hourly',
            'minute': minute,
            'job': job,
            'created': datetime.now().isoformat()
        }
        self.save_schedules()
        print(f"Added hourly schedule '{schedule_id}' at minute {minute}")
    
    def add_daily_schedule(self, schedule_id: str, hour: int = 9, minute: int = 0):
        """
        Add a daily schedule.
        
        Args:
            schedule_id: Unique identifier for this schedule
            hour: Hour of the day to trigger (0-23)
            minute: Minute of the hour to trigger (0-59)
        """
        job = schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self._take_scheduled_snapshot, schedule_id)
        self.schedules[schedule_id] = {
            'type': 'daily',
            'hour': hour,
            'minute': minute,
            'job': job,
            'created': datetime.now().isoformat()
        }
        self.save_schedules()
        print(f"Added daily schedule '{schedule_id}' at {hour:02d}:{minute:02d}")
    
    def add_weekly_schedule(self, schedule_id: str, day_of_week: str, hour: int = 9, minute: int = 0):
        """
        Add a weekly schedule.
        
        Args:
            schedule_id: Unique identifier for this schedule
            day_of_week: Day of the week ('monday', 'tuesday', etc.)
            hour: Hour of the day to trigger (0-23)
            minute: Minute of the hour to trigger (0-59)
        """
        day_method = getattr(schedule.every(), day_of_week.lower())
        job = day_method.at(f"{hour:02d}:{minute:02d}").do(self._take_scheduled_snapshot, schedule_id)
        self.schedules[schedule_id] = {
            'type': 'weekly',
            'day_of_week': day_of_week,
            'hour': hour,
            'minute': minute,
            'job': job,
            'created': datetime.now().isoformat()
        }
        self.save_schedules()
        print(f"Added weekly schedule '{schedule_id}' on {day_of_week} at {hour:02d}:{minute:02d}")
    
    def add_custom_interval(self, schedule_id: str, minutes: int):
        """
        Add a custom interval schedule.
        
        Args:
            schedule_id: Unique identifier for this schedule
            minutes: Interval in minutes
        """
        job = schedule.every(minutes).minutes.do(self._take_scheduled_snapshot, schedule_id)
        self.schedules[schedule_id] = {
            'type': 'interval',
            'minutes': minutes,
            'job': job,
            'created': datetime.now().isoformat()
        }
        self.save_schedules()
        print(f"Added interval schedule '{schedule_id}' every {minutes} minutes")
    
    def remove_schedule(self, schedule_id: str):
        """Remove a schedule."""
        if schedule_id in self.schedules:
            schedule.cancel_job(self.schedules[schedule_id]['job'])
            del self.schedules[schedule_id]
            self.save_schedules()
            print(f"Removed schedule '{schedule_id}'")
        else:
            print(f"Schedule '{schedule_id}' not found")
    
    def get_all_schedules(self) -> Dict[str, Dict]:
        """Get all active schedules."""
        return self.schedules.copy()
    
    def clear_all_schedules(self):
        """Clear all schedules."""
        schedule.clear()
        self.schedules.clear()
        self.save_schedules()
        print("Cleared all schedules")
    
    def _take_scheduled_snapshot(self, schedule_id: str):
        """Take a snapshot as part of a scheduled task."""
        try:
            print(f"Taking scheduled snapshot for '{schedule_id}'...")
            snapshot_data = self.snapshot_callback()
            
            # Add automation metadata
            snapshot_data.update({
                'automation_schedule_id': schedule_id,
                'automation_timestamp': datetime.now().isoformat(),
                'automation_type': self.schedules.get(schedule_id, {}).get('type', 'unknown')
            })
            
            # TODO: Save to database
            # self.save_to_database(snapshot_data)
            
            print(f"Scheduled snapshot completed for '{schedule_id}': {snapshot_data['people_count']} people at {snapshot_data['timestamp']}")
            
        except Exception as e:
            print(f"Error taking scheduled snapshot for '{schedule_id}': {e}")
    
    def save_schedules(self):
        """Save schedules to file."""
        try:
            # Convert job objects to serializable data
            serializable_schedules = {}
            for schedule_id, schedule_data in self.schedules.items():
                serializable_schedules[schedule_id] = {
                    k: v for k, v in schedule_data.items() 
                    if k != 'job'  # Skip the job object
                }
            
            with open(self.schedule_file, 'w') as f:
                json.dump(serializable_schedules, f, indent=2)
        except Exception as e:
            print(f"Error saving schedules: {e}")
    
    def load_schedules(self):
        """Load schedules from file."""
        try:
            if os.path.exists(self.schedule_file):
                with open(self.schedule_file, 'r') as f:
                    saved_schedules = json.load(f)
                
                # Recreate schedules
                for schedule_id, schedule_data in saved_schedules.items():
                    if schedule_data['type'] == 'hourly':
                        self.add_hourly_schedule(schedule_id, schedule_data['minute'])
                    elif schedule_data['type'] == 'daily':
                        self.add_daily_schedule(schedule_id, schedule_data['hour'], schedule_data['minute'])
                    elif schedule_data['type'] == 'weekly':
                        self.add_weekly_schedule(schedule_id, schedule_data['day_of_week'], 
                                               schedule_data['hour'], schedule_data['minute'])
                    elif schedule_data['type'] == 'interval':
                        self.add_custom_interval(schedule_id, schedule_data['minutes'])
                
                print(f"Loaded {len(saved_schedules)} schedules from file")
        except Exception as e:
            print(f"Error loading schedules: {e}")
    
    def get_next_run_times(self) -> Dict[str, str]:
        """Get next run times for all schedules."""
        next_runs = {}
        for schedule_id, schedule_data in self.schedules.items():
            try:
                job = schedule_data['job']
                next_run = job.next_run
                if next_run:
                    next_runs[schedule_id] = next_run.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    next_runs[schedule_id] = "Not scheduled"
            except:
                next_runs[schedule_id] = "Unknown"
        return next_runs


# Example usage and testing
if __name__ == "__main__":
    def mock_snapshot_callback():
        """Mock snapshot callback for testing."""
        return {
            'people_count': 5,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'datetime_obj': datetime.now()
        }
    
    # Create scheduler
    scheduler = AutomationScheduler(mock_snapshot_callback)
    
    # Add some test schedules
    scheduler.add_hourly_schedule("hourly_test", minute=30)
    scheduler.add_daily_schedule("daily_test", hour=9, minute=0)
    scheduler.add_weekly_schedule("weekly_test", "monday", hour=8, minute=0)
    scheduler.add_custom_interval("interval_test", minutes=5)
    
    # Start scheduler
    scheduler.start_scheduler()
    
    print("Automation scheduler running...")
    print("Schedules:", scheduler.get_all_schedules())
    print("Next runs:", scheduler.get_next_run_times())
    
    try:
        # Keep running for demonstration
        time.sleep(30)  # Run for 30 seconds
    except KeyboardInterrupt:
        print("Stopping scheduler...")
    finally:
        scheduler.stop_scheduler()

