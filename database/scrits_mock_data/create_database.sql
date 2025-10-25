-- ============================================
-- Course Scheduling Database Schema - SQLite
-- ============================================

-- Enable foreign key constraints (important for SQLite)
PRAGMA foreign_keys = ON;

-- ============================================
-- LOGIN MODULE
-- ============================================

-- Table: role
CREATE TABLE IF NOT EXISTS role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(45) NOT NULL UNIQUE
);

-- Table: user
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(300) NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(role_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ============================================
-- DATA MODULE
-- ============================================

-- Table: building
CREATE TABLE IF NOT EXISTS building (
    building_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL UNIQUE
);

-- Table: room
CREATE TABLE IF NOT EXISTS room (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    number VARCHAR(20) NOT NULL,
    building_id INTEGER NOT NULL,
    capacity INTEGER CHECK(capacity > 0),
    FOREIGN KEY (building_id) REFERENCES building(building_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    UNIQUE(building_id, number)
);

-- Table: course
CREATE TABLE IF NOT EXISTS course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    instructor VARCHAR(200),
    department VARCHAR(200)
);

-- Table: class_schedule
CREATE TABLE IF NOT EXISTS class_schedule (
    class_schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    day_of_week VARCHAR(1) NOT NULL CHECK(day_of_week IN ('M','T','W','R','F')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    semester VARCHAR(45) NOT NULL,
    FOREIGN KEY (room_id) REFERENCES room(room_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CHECK(start_time < end_time)
);

-- Table: raw_data
CREATE TABLE IF NOT EXISTS raw_data (
    data_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    room_count INTEGER NOT NULL CHECK(room_count >= 0),
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(room_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_user_role ON user(role_id);
CREATE INDEX IF NOT EXISTS idx_room_building ON room(building_id);
CREATE INDEX IF NOT EXISTS idx_schedule_room ON class_schedule(room_id);
CREATE INDEX IF NOT EXISTS idx_schedule_course ON class_schedule(course_id);
CREATE INDEX IF NOT EXISTS idx_rawdata_room ON raw_data(room_id);
CREATE INDEX IF NOT EXISTS idx_user_username ON user(username);
CREATE INDEX IF NOT EXISTS idx_rawdata_timestamp ON raw_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_schedule_semester ON class_schedule(semester);
