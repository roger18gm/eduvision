import sqlite3


class Database:
    def __init__(self, db_path="./database/eduvisiondb.db"):
        self.conn = sqlite3.connect(db_path)
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
