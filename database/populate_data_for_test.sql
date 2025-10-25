-- ============================================
-- BYU-Idaho Database - Sample Data Population
-- ============================================

-- IMPORTANT: Run this AFTER creating the database schema

-- ============================================
-- ROLES (Fake but realistic)
-- ============================================

INSERT INTO role (name) VALUES 
    ('Admin'),
    ('Faculty'),
    ('Student'),
    ('Staff');

-- ============================================
-- USERS (Fake data with hashed-style passwords)
-- ============================================

INSERT INTO user (username, password, role_id) VALUES 
    -- Admins
    ('admin', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 1),
    ('j.smith', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 1),
    
    -- Faculty
    ('dr.johnson', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 2),
    ('prof.williams', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 2),
    ('dr.brown', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 2),
    ('prof.davis', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 2),
    ('dr.martinez', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 2),
    
    -- Students
    ('student1', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 3),
    ('student2', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 3),
    ('student3', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 3),
    
    -- Staff
    ('facilities.manager', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 4);

-- ============================================
-- BUILDINGS (Real BYU-Idaho Buildings)
-- ============================================

INSERT INTO building (name) VALUES 
    ('Smith Building'),                          -- Business & Accounting
    ('Snow Building'),                           -- Performing Arts
    ('Romney Building'),                         -- Sciences
    ('Clarke Building'),                         -- Various departments
    ('Hinckley Building'),                       -- Multi-purpose
    ('Taylor Building'),                         -- Various classrooms
    ('Spori Building'),                          -- Various departments
    ('Ricks Building'),                          -- Math, Psychology, etc.
    ('McKay Library'),                           -- Library
    ('BYU-Idaho Center'),                        -- Large events/classes
    ('Austin Building'),                         -- Technical & Engineering
    ('Benson Building'),                         -- Agriculture & Biology
    ('Science and Technology Center');           -- Science & Technology

-- ============================================
-- ROOMS (Representative sample rooms)
-- ============================================

-- Smith Building (Business)
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 1, 35),
    ('102', 1, 40),
    ('205', 1, 30),
    ('210', 1, 45),
    ('301', 1, 25);

-- Snow Building (Performing Arts)
INSERT INTO room (number, building_id, capacity) VALUES 
    ('Barrus Concert Hall', 2, 450),
    ('103', 2, 30),
    ('201', 2, 25),
    ('Theater', 2, 200);

-- Romney Building (Sciences)
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 3, 40),
    ('125', 3, 35),
    ('201', 3, 30),
    ('Lab-210', 3, 24),
    ('305', 3, 45);

-- Clarke Building
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 4, 35),
    ('204', 4, 40),
    ('310', 4, 30);

-- Hinckley Building
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 5, 50),
    ('202', 5, 45),
    ('310', 5, 40),
    ('405', 5, 35);

-- Taylor Building
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 6, 40),
    ('205', 6, 35),
    ('301', 6, 30),
    ('350', 6, 45);

-- Spori Building
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 7, 40),
    ('215', 7, 35),
    ('304', 7, 30);

-- Ricks Building
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 8, 45),
    ('203', 8, 40),
    ('310', 8, 35),
    ('401', 8, 30);

-- McKay Library
INSERT INTO room (number, building_id, capacity) VALUES 
    ('Study Room 101', 9, 8),
    ('Study Room 201', 9, 12),
    ('Conference Room', 9, 20);

-- BYU-Idaho Center
INSERT INTO room (number, building_id, capacity) VALUES 
    ('Main Arena', 10, 3000),
    ('Room 101', 10, 50),
    ('Room 205', 10, 60);

-- Austin Building (Engineering)
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 11, 35),
    ('Lab-150', 11, 24),
    ('205', 11, 40);

-- Benson Building (Ag & Bio)
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 12, 40),
    ('Lab-120', 12, 24),
    ('210', 12, 35);

-- Science and Technology Center
INSERT INTO room (number, building_id, capacity) VALUES 
    ('101', 13, 45),
    ('Lab-201', 13, 30),
    ('305', 13, 40),
    ('410', 13, 35);

-- ============================================
-- COURSES (Real BYU-Idaho style courses)
-- ============================================

INSERT INTO course (course_code, name, instructor, department) VALUES 
    -- Computer Science
    ('CIT 111', 'Introduction to Databases', 'Dr. Johnson', 'Computer Science'),
    ('CIT 160', 'Introduction to Programming', 'Prof. Williams', 'Computer Science'),
    ('CIT 260', 'Object-Oriented Programming', 'Dr. Johnson', 'Computer Science'),
    ('CS 213', 'Web Engineering I', 'Prof. Martinez', 'Computer Science'),
    
    -- Business
    ('BUS 101', 'Introduction to Business', 'Prof. Davis', 'Business'),
    ('ACCT 201', 'Principles of Accounting I', 'Dr. Brown', 'Business'),
    ('ACCT 202', 'Principles of Accounting II', 'Dr. Brown', 'Business'),
    ('MGT 301', 'Organizational Behavior', 'Prof. Davis', 'Business'),
    
    -- Mathematics
    ('MATH 108', 'College Algebra', 'Dr. Thompson', 'Mathematics'),
    ('MATH 112', 'Calculus I', 'Dr. Anderson', 'Mathematics'),
    ('MATH 113', 'Calculus II', 'Dr. Anderson', 'Mathematics'),
    ('MATH 221', 'Statistics I', 'Prof. Lee', 'Mathematics'),
    
    -- Sciences
    ('CHEM 101', 'General Chemistry I', 'Dr. Wilson', 'Chemistry'),
    ('BIO 100', 'Biology Foundations', 'Prof. Garcia', 'Biology'),
    ('PHYS 121', 'Physics I', 'Dr. Taylor', 'Physics'),
    
    -- Communications
    ('COMM 101', 'Communication Foundations', 'Prof. Roberts', 'Communications'),
    ('FDENG 101', 'Writing & Reasoning Foundations', 'Dr. Clark', 'English'),
    
    -- Religion
    ('REL 200', 'The Eternal Family', 'Prof. White', 'Religious Education'),
    ('REL 275', 'Teachings & Doctrine of the Book of Mormon', 'Prof. Harris', 'Religious Education'),
    
    -- Music
    ('MUSIC 101', 'Music Fundamentals', 'Prof. Young', 'Music'),
    ('MUSIC 160', 'Concert Choir', 'Dr. King', 'Music');

-- ============================================
-- CLASS SCHEDULES (Fall 2024 semester)
-- ============================================

-- CIT 111 - Multiple sections
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (1, 1, 'M', '08:00:00', '08:50:00', 'Fall 2024'),
    (1, 1, 'W', '08:00:00', '08:50:00', 'Fall 2024'),
    (1, 1, 'F', '08:00:00', '08:50:00', 'Fall 2024'),
    (2, 1, 'T', '10:00:00', '10:50:00', 'Fall 2024'),
    (2, 1, 'R', '10:00:00', '10:50:00', 'Fall 2024');

-- CIT 160
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (3, 2, 'M', '09:00:00', '09:50:00', 'Fall 2024'),
    (3, 2, 'W', '09:00:00', '09:50:00', 'Fall 2024'),
    (3, 2, 'F', '09:00:00', '09:50:00', 'Fall 2024');

-- CIT 260
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (4, 3, 'T', '14:00:00', '15:15:00', 'Fall 2024'),
    (4, 3, 'R', '14:00:00', '15:15:00', 'Fall 2024');

-- CS 213
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (5, 4, 'M', '13:00:00', '13:50:00', 'Fall 2024'),
    (5, 4, 'W', '13:00:00', '13:50:00', 'Fall 2024'),
    (5, 4, 'F', '13:00:00', '13:50:00', 'Fall 2024');

-- BUS 101
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (1, 5, 'T', '11:00:00', '11:50:00', 'Fall 2024'),
    (1, 5, 'R', '11:00:00', '11:50:00', 'Fall 2024');

-- ACCT 201
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (2, 6, 'M', '10:00:00', '10:50:00', 'Fall 2024'),
    (2, 6, 'W', '10:00:00', '10:50:00', 'Fall 2024'),
    (2, 6, 'F', '10:00:00', '10:50:00', 'Fall 2024');

-- ACCT 202
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (3, 7, 'T', '09:00:00', '09:50:00', 'Fall 2024'),
    (3, 7, 'R', '09:00:00', '09:50:00', 'Fall 2024');

-- MGT 301
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (4, 8, 'M', '15:00:00', '16:15:00', 'Fall 2024'),
    (4, 8, 'W', '15:00:00', '16:15:00', 'Fall 2024');

-- MATH 108
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (29, 9, 'M', '08:00:00', '08:50:00', 'Fall 2024'),
    (29, 9, 'W', '08:00:00', '08:50:00', 'Fall 2024'),
    (29, 9, 'F', '08:00:00', '08:50:00', 'Fall 2024');

-- MATH 112
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (30, 10, 'T', '08:00:00', '08:50:00', 'Fall 2024'),
    (30, 10, 'R', '08:00:00', '08:50:00', 'Fall 2024');

-- MATH 113
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (31, 11, 'M', '11:00:00', '11:50:00', 'Fall 2024'),
    (31, 11, 'W', '11:00:00', '11:50:00', 'Fall 2024'),
    (31, 11, 'F', '11:00:00', '11:50:00', 'Fall 2024');

-- MATH 221
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (32, 12, 'T', '13:00:00', '14:15:00', 'Fall 2024'),
    (32, 12, 'R', '13:00:00', '14:15:00', 'Fall 2024');

-- CHEM 101
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (14, 13, 'M', '09:00:00', '09:50:00', 'Fall 2024'),
    (14, 13, 'W', '09:00:00', '09:50:00', 'Fall 2024'),
    (14, 13, 'F', '09:00:00', '09:50:00', 'Fall 2024');

-- BIO 100
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (44, 14, 'T', '10:00:00', '11:15:00', 'Fall 2024'),
    (44, 14, 'R', '10:00:00', '11:15:00', 'Fall 2024');

-- PHYS 121
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (48, 15, 'M', '14:00:00', '14:50:00', 'Fall 2024'),
    (48, 15, 'W', '14:00:00', '14:50:00', 'Fall 2024'),
    (48, 15, 'F', '14:00:00', '14:50:00', 'Fall 2024');

-- COMM 101
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (21, 16, 'T', '14:00:00', '14:50:00', 'Fall 2024'),
    (21, 16, 'R', '14:00:00', '14:50:00', 'Fall 2024');

-- FDENG 101
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (22, 17, 'M', '10:00:00', '10:50:00', 'Fall 2024'),
    (22, 17, 'W', '10:00:00', '10:50:00', 'Fall 2024'),
    (22, 17, 'F', '10:00:00', '10:50:00', 'Fall 2024');

-- REL 200
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (23, 18, 'T', '09:00:00', '09:50:00', 'Fall 2024'),
    (23, 18, 'R', '09:00:00', '09:50:00', 'Fall 2024');

-- REL 275
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (24, 19, 'M', '12:00:00', '12:50:00', 'Fall 2024'),
    (24, 19, 'W', '12:00:00', '12:50:00', 'Fall 2024'),
    (24, 19, 'F', '12:00:00', '12:50:00', 'Fall 2024');

-- MUSIC 101
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (7, 20, 'T', '11:00:00', '11:50:00', 'Fall 2024'),
    (7, 20, 'R', '11:00:00', '11:50:00', 'Fall 2024');

-- MUSIC 160 (Concert Choir)
INSERT INTO class_schedule (room_id, course_id, day_of_week, start_time, end_time, semester) VALUES 
    (6, 21, 'M', '16:00:00', '17:15:00', 'Fall 2024'),
    (6, 21, 'W', '16:00:00', '17:15:00', 'Fall 2024');

-- ============================================
-- RAW DATA (Sample occupancy data)
-- ============================================

-- Sample occupancy readings for various rooms
INSERT INTO raw_data (room_id, room_count, timestamp) VALUES 
    -- Smith 101 - Monday morning class
    (1, 32, '2024-10-21 08:05:00'),
    (1, 34, '2024-10-21 08:30:00'),
    (1, 33, '2024-10-21 08:45:00'),
    (1, 0, '2024-10-21 09:00:00'),
    
    -- Smith 102 - Tuesday class
    (2, 38, '2024-10-22 10:05:00'),
    (2, 39, '2024-10-22 10:30:00'),
    (2, 36, '2024-10-22 10:45:00'),
    
    -- Romney 101 - Chemistry lab
    (11, 24, '2024-10-21 09:10:00'),
    (11, 24, '2024-10-21 09:30:00'),
    (11, 23, '2024-10-21 09:45:00'),
    
    -- McKay Library Study Rooms
    (33, 6, '2024-10-21 14:00:00'),
    (33, 8, '2024-10-21 15:00:00'),
    (34, 10, '2024-10-21 14:30:00'),
    (34, 12, '2024-10-21 16:00:00'),
    
    -- BYU-I Center large class
    (36, 450, '2024-10-22 11:00:00'),
    (36, 455, '2024-10-22 11:30:00'),
    
    -- Various other readings
    (5, 23, '2024-10-23 13:05:00'),
    (8, 28, '2024-10-23 10:15:00'),
    (15, 45, '2024-10-23 08:30:00'),
    (20, 32, '2024-10-23 15:10:00');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Count records in each table
SELECT 'Roles' as table_name, COUNT(*) as count FROM role
UNION ALL
SELECT 'Users', COUNT(*) FROM user
UNION ALL
SELECT 'Buildings', COUNT(*) FROM building
UNION ALL
SELECT 'Rooms', COUNT(*) FROM room
UNION ALL
SELECT 'Courses', COUNT(*) FROM course
UNION ALL
SELECT 'Class Schedules', COUNT(*) FROM class_schedule
UNION ALL
SELECT 'Raw Data', COUNT(*) FROM raw_data;