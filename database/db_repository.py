import sqlite3
import sys
import os


class Database:
    def __init__(self, db_path="./database/eduvisiondb.db"):
        # Handle bundled app paths
        if getattr(sys, 'frozen', False):
            # Running as bundled exe
            print("Running as bundled executable")
            base_path = sys._MEIPASS
        else:
            # Running as script
            print("Running as script")
            base_path = os.path.dirname(
                os.path.dirname(__file__))  # Project root
        full_path = os.path.join(base_path, db_path)
        self.conn = sqlite3.connect(full_path)
        self.conn.row_factory = sqlite3.Row

    def get_buildings(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT building_id, name FROM building")
        return [dict(row) for row in cursor.fetchall()]

    def get_building(self, building_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT building_id, name FROM building WHERE building_id = ?", (building_id,))
        return dict(cursor.fetchone())

    def get_room(self, room_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT room_id, number, capacity, building_id FROM room WHERE room_id = ?", (room_id,))
        return dict(cursor.fetchone())

    def get_rooms_by_building(self, building_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT room_id, number FROM room WHERE building_id = ?", (building_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_room_capacity(self, room_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT capacity FROM room WHERE room_id = ?", (room_id,))
        return cursor.fetchone()[0]

    def save_snapshot(self, room_id, timestamp, count):
        cursor = self.conn.cursor()  # timestamp is CURRENT_TIMESTAMP
        cursor.execute(
            "INSERT INTO raw_data (room_id, timestamp, room_count) VALUES (?, ?, ?)",
            (room_id, timestamp, count)
        )
        self.conn.commit()

    def get_all_course_names(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM course")
        return [row['name'] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()

    def get_class_schedules(self, room_id=None, course_id=None, start_date=None, end_date=None):
        cursor = self.conn.cursor()
        query = "SELECT * FROM class_schedule WHERE 1=1"
        params = []
        if room_id is not None:
            query += " AND room_id = ?"
            params.append(room_id)
        if course_id is not None:
            query += " AND course_id = ?"
            params.append(course_id)
        if start_date is not None:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date is not None:
            query += " AND timestamp <= ?"
            params.append(end_date)
        cursor.execute(query, tuple(params))
        return [dict(row) for row in cursor.fetchall()]

    def get_all_courses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT course_id, name FROM course")
        return [dict(row) for row in cursor.fetchall()]
