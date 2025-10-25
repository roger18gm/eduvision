import sqlite3


class Database:
    def __init__(self, db_path="./database/eduvisiondb.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def get_buildings(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT building_id, name FROM building")
        return [dict(row) for row in cursor.fetchall()]

    def get_rooms_by_building(self, building_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT room_id, number FROM room WHERE building_id = ?", (building_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_room_capacity(self, room_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT capacity FROM room WHERE room_id = ?", (room_id,))
        return cursor.fetchone()[0]

    def close(self):
        self.conn.close()
