# Database Documentation

## Overview

This document describes the database schema for the course scheduling and room management system. The system manages users, roles, buildings, rooms, courses, class schedules, and raw occupancy data.

## Database Schema

### Login Module

#### Table: `user`

Stores user account information for system authentication and authorization.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INT | PRIMARY KEY | Unique identifier for each user |
| username | VARCHAR(100) | | User's login name |
| password | VARCHAR(300) | | Encrypted password for authentication |
| role_id | INT | FOREIGN KEY | References role table |

**Relationships:**
- Many-to-One with `role` table

---

#### Table: `role`

Defines user roles and permissions within the system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| role_id | INT | PRIMARY KEY | Unique identifier for each role |
| name | VARCHAR(45) | | Role name (e.g., Admin, Instructor, Student) |

**Relationships:**
- One-to-Many with `user` table

---

### Data Module

#### Table: `building`

Contains information about campus buildings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| building_id | INT | PRIMARY KEY | Unique identifier for each building |
| name | VARCHAR(200) | | Building name |

**Relationships:**
- One-to-Many with `room` table

---

#### Table: `room`

Stores details about individual rooms within buildings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| room_id | INT | PRIMARY KEY | Unique identifier for each room |
| number | INT | | Room number within the building |
| building_id | INT | FOREIGN KEY | References building table |
| capacity | INT | | Maximum occupancy capacity of the room |

**Relationships:**
- Many-to-One with `building` table
- One-to-Many with `class_schedule` table
- One-to-Many with `raw_data` table

---

#### Table: `course`

Contains course information offered by the institution.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| course_id | INT | PRIMARY KEY | Unique identifier for each course |
| course_code | VARCHAR(100) | | Official course code |
| name | VARCHAR(100) | | Course name |
| instructor | VARCHAR(200) | | Instructor name for the course |
| department | VARCHAR(200) | | Academic department offering the course |

**Relationships:**
- One-to-Many with `class_schedule` table

---

#### Table: `class_schedule`

Manages scheduled class sessions linking courses to rooms and time slots.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| class_schedule_id | INT | PRIMARY KEY | Unique identifier for each scheduled class |
| room_id | INT | FOREIGN KEY | References room table |
| course_id | INT | FOREIGN KEY | References course table |
| day_of_week | ENUM('M','T','W','R','F') | | Day when class meets (M=Monday, T=Tuesday, W=Wednesday, R=Thursday, F=Friday) |
| start_time | TIME | | Class start time (format: HH:MM:SS) |
| end_time | TIME | | Class end time (format: HH:MM:SS) |
| semester | VARCHAR(45) | | Academic semester (e.g., Fall 2024, Spring 2025) |

**Relationships:**
- Many-to-One with `room` table
- Many-to-One with `course` table

---

#### Table: `raw_data`

Stores raw occupancy data collected from sensors or manual counts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| data_id | INT | PRIMARY KEY | Unique identifier for each data entry |
| room_id | INT | FOREIGN KEY | References room table |
| room_count | INT | | Number of people counted in the room |
| timestamp | DATETIME | | Date and time of the data collection |

**Relationships:**
- Many-to-One with `room` table

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

## Additional Recommendations

Here are some other data type improvements to consider:

### Suggested Changes:

1. **`semester` field** (class_schedule table):
   - Current: `VARCHAR(45)`
   - **Option A:** `ENUM('Fall 2024', 'Spring 2025', ...)` - Limited but ensures consistency
   - **Option B:** Keep VARCHAR(45) - More flexible for future semesters
   - **Option C:** Split into two fields: `term ENUM('Fall','Spring','Summer')` + `year YEAR` - Easier to query by term or year

2. **Primary Keys:**
   - Current: `INT`
   - Consider: `INT AUTO_INCREMENT` - Automatically generates unique IDs

3. **`capacity` field** (room table):
   - Current: `INT`
   - Consider: `SMALLINT UNSIGNED` - Rooms unlikely to exceed 65,535 capacity, saves space
   - Or: `TINYINT UNSIGNED` if capacity never exceeds 255

4. **`room_count` field** (raw_data table):
   - Current: `INT`
   - Consider: `SMALLINT UNSIGNED` - Matches room capacity constraints

5. **`number` field** (room table):
   - Current: `INT`
   - Consider: `VARCHAR(20)` - Allows room numbers like "101A", "B-205", "Lab-3"

6. **Name fields:**
   - Consider adding `NOT NULL` constraints where appropriate
   - `building.name`, `course.name`, `course.course_code` should probably be required

**What would you like to change? Should I update the documentation with any of these suggestions?**

---

## Notes

- Time fields now use proper TIME datatype for accurate time operations
- `day_of_week` uses ENUM for data validation and storage efficiency
- `timestamp` uses DATETIME for proper date/time operations and indexing
- Password field is VARCHAR(300) to accommodate encrypted/hashed passwords
- The schema supports multi-building campus environments
- Raw data collection enables occupancy analysis and space utilization reporting

---

## Usage Considerations

### Security
- Passwords should always be hashed before storage
- Role-based access control (RBAC) is implemented through the user-role relationship

### Data Integrity
- Foreign key constraints ensure referential integrity
- Consider adding unique constraints on username in the user table
- Consider composite unique constraints on (building_id, number) in the room table

### Performance
- Add indexes on frequently queried foreign keys
- Consider indexing timestamp fields for temporal queries
- Index username for faster login lookups

---

*Last Updated: October 2025*