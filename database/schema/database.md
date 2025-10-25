# Database Documentation

## Overview

This document describes the database schema for the course scheduling and room management system. The system manages users, roles, buildings, rooms, courses, class schedules, and raw occupancy data.

## Database Schema

### Login Module

#### Table: `role`

Defines user roles and permissions within the system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| role_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each role |
| name | VARCHAR(45) | NOT NULL UNIQUE | Role name (e.g., Admin, Faculty, Student, Staff) |

**Relationships:**
- One-to-Many with `user` table

---

#### Table: `user`

Stores user account information for system authentication and authorization.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each user |
| username | VARCHAR(100) | NOT NULL UNIQUE | User's login name |
| password | VARCHAR(300) | NOT NULL | Encrypted password for authentication |
| role_id | INTEGER | FOREIGN KEY, NOT NULL | References role table |

**Relationships:**
- Many-to-One with `role` table (ON DELETE RESTRICT, ON UPDATE CASCADE)

---

### Data Module

#### Table: `building`

Contains information about campus buildings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| building_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each building |
| name | VARCHAR(200) | NOT NULL UNIQUE | Building name (e.g., Smith Building, Snow Building) |

**Relationships:**
- One-to-Many with `room` table

---

#### Table: `room`

Stores details about individual rooms within buildings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| room_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each room |
| number | VARCHAR(20) | NOT NULL | Room number within the building (e.g., "101", "Lab-210") |
| building_id | INTEGER | FOREIGN KEY, NOT NULL | References building table |
| capacity | INTEGER | CHECK(capacity > 0) | Maximum occupancy capacity of the room |

**Relationships:**
- Many-to-One with `building` table (ON DELETE RESTRICT, ON UPDATE CASCADE)
- One-to-Many with `class_schedule` table
- One-to-Many with `raw_data` table

**Additional Constraints:**
- UNIQUE constraint on (building_id, number) combination

---

#### Table: `course`

Contains course information offered by the institution.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| course_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each course |
| course_code | VARCHAR(100) | NOT NULL UNIQUE | Official course code (e.g., CIT 111, MATH 112) |
| name | VARCHAR(100) | NOT NULL | Course name |
| instructor | VARCHAR(200) | | Instructor name for the course |
| department | VARCHAR(200) | | Academic department offering the course |

**Relationships:**
- One-to-Many with `class_schedule` table

---

#### Table: `class_schedule`

Manages scheduled class sessions linking courses to rooms and time slots.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| class_schedule_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each scheduled class |
| room_id | INTEGER | FOREIGN KEY, NOT NULL | References room table |
| course_id | INTEGER | FOREIGN KEY, NOT NULL | References course table |
| day_of_week | VARCHAR(1) | NOT NULL, CHECK(IN 'M','T','W','R','F') | Day when class meets (M=Monday, T=Tuesday, W=Wednesday, R=Thursday, F=Friday) |
| start_time | TIME | NOT NULL | Class start time (format: HH:MM:SS) |
| end_time | TIME | NOT NULL | Class end time (format: HH:MM:SS) |
| semester | VARCHAR(10) | NOT NULL, CHECK(IN 'Fall','Winter','Spring','Summer') | Academic term (Fall, Winter, Spring, Summer) |
| year | INTEGER | NOT NULL | Academic year (e.g., 2024, 2025) |
| start_date | DATE | | Semester start date (format: YYYY-MM-DD) |
| end_date | DATE | | Semester end date (format: YYYY-MM-DD) |

**Relationships:**
- Many-to-One with `room` table (ON DELETE RESTRICT, ON UPDATE CASCADE)
- Many-to-One with `course` table (ON DELETE RESTRICT, ON UPDATE CASCADE)

**Additional Constraints:**
- CHECK constraint: start_time < end_time

---

#### Table: `raw_data`

Stores raw occupancy data collected from sensors or manual counts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| data_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique identifier for each data entry |
| room_id | INTEGER | FOREIGN KEY, NOT NULL | References room table |
| room_count | INTEGER | NOT NULL, CHECK(room_count >= 0) | Number of people counted in the room |
| timestamp | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Date and time of the data collection |

**Relationships:**
- Many-to-One with `room` table (ON DELETE CASCADE, ON UPDATE CASCADE)

---

## Entity Relationships

### Key Relationships Summary

1. **User Authentication Flow:**
   - `user` → `role`: Each user is assigned one role that determines their permissions

2. **Physical Infrastructure:**
   - `building` → `room`: Buildings contain multiple rooms

3. **Academic Scheduling:**
   - `course` → `class_schedule`: Courses are scheduled into specific time slots
   - `room` → `class_schedule`: Rooms host scheduled classes
   - Both course and room information combine to create the complete class schedule

4. **Occupancy Tracking:**
   - `room` → `raw_data`: Rooms have occupancy data collected over time

---

*Last Updated: October 2024*  
*Database: eduvisiondb.db*  
*DBMS: SQLite 3*