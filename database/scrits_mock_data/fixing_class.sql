-- ============================================
-- Migrate semester column to semester + year columns
-- ============================================

-- Step 1: Add new columns
ALTER TABLE class_schedule ADD COLUMN semester VARCHAR(10) CHECK(semester IN ('Fall','Winter','Spring','Summer'));
ALTER TABLE class_schedule ADD COLUMN year INTEGER;

-- Step 2: Migrate existing data from old 'Fall 2024' format to semester='Fall' and year=2024
-- Note: We're using a temporary column name first to avoid conflicts
UPDATE class_schedule 
SET year = 2024
WHERE semester LIKE '%2024%' OR semester = 'Fall 2024';

-- Since SQLite doesn't allow us to have two columns with same name during migration,
-- we need to use a different approach

-- Step 3: Create a temporary table with the new structure
CREATE TABLE class_schedule_new (
    class_schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    day_of_week VARCHAR(1) NOT NULL CHECK(day_of_week IN ('M','T','W','R','F')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    semester VARCHAR(10) NOT NULL CHECK(semester IN ('Fall','Winter','Spring','Summer')),
    year INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (room_id) REFERENCES room(room_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CHECK(start_time < end_time)
);

-- Step 4: Copy data to new table, extracting semester and year from old format
INSERT INTO class_schedule_new 
    (class_schedule_id, room_id, course_id, day_of_week, start_time, end_time, semester, year, start_date, end_date)
SELECT 
    class_schedule_id, 
    room_id, 
    course_id, 
    day_of_week, 
    start_time, 
    end_time,
    CASE 
        WHEN old.semester LIKE 'Fall%' THEN 'Fall'
        WHEN old.semester LIKE 'Winter%' THEN 'Winter'
        WHEN old.semester LIKE 'Spring%' THEN 'Spring'
        WHEN old.semester LIKE 'Summer%' THEN 'Summer'
        ELSE 'Fall'  -- default fallback
    END as semester,
    CASE 
        WHEN old.semester LIKE '%2024%' THEN 2024
        WHEN old.semester LIKE '%2025%' THEN 2025
        ELSE 2024  -- default fallback
    END as year,
    start_date, 
    end_date
FROM class_schedule as old;

-- Step 5: Drop old table
DROP TABLE class_schedule;

-- Step 6: Rename new table to original name
ALTER TABLE class_schedule_new RENAME TO class_schedule;

-- Step 7: Recreate indexes
CREATE INDEX IF NOT EXISTS idx_schedule_room ON class_schedule(room_id);
CREATE INDEX IF NOT EXISTS idx_schedule_course ON class_schedule(course_id);
CREATE INDEX IF NOT EXISTS idx_schedule_semester_year ON class_schedule(semester, year);

-- ============================================
-- Verification Queries
-- ============================================

-- Check table structure
PRAGMA table_info(class_schedule);

-- Verify data migration
SELECT 
    'After migration' as status,
    COUNT(*) as total_records,
    COUNT(DISTINCT semester) as unique_semesters,
    COUNT(DISTINCT year) as unique_years
FROM class_schedule;

-- Sample records
SELECT 
    class_schedule_id,
    course_id,
    day_of_week,
    start_time,
    end_time,
    semester,
    year,
    start_date,
    end_date
FROM class_schedule
LIMIT 10;

-- Count by semester and year
SELECT 
    semester,
    year,
    COUNT(*) as class_count
FROM class_schedule
GROUP BY semester, year
ORDER BY year, 
    CASE semester 
        WHEN 'Winter' THEN 1 
        WHEN 'Spring' THEN 2 
        WHEN 'Summer' THEN 3 
        WHEN 'Fall' THEN 4 
    END;