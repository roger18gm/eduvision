-- ============================================
-- Add start_date and end_date columns to class_schedule
-- ============================================

-- Add the new columns
ALTER TABLE class_schedule ADD COLUMN start_date DATE;
ALTER TABLE class_schedule ADD COLUMN end_date DATE;

-- ============================================
-- Update existing records with Fall 2024 dates
-- Fall 2024 semester: September 3, 2024 - December 14, 2024
-- ============================================

UPDATE class_schedule 
SET start_date = '2024-09-03',
    end_date = '2024-12-14'
WHERE semester = 'Fall 2024';

-- ============================================
-- Verify the changes
-- ============================================

-- Check the table structure
PRAGMA table_info(class_schedule);

-- View sample records with new dates
SELECT 
    class_schedule_id,
    course_id,
    day_of_week,
    start_time,
    end_time,
    semester,
    start_date,
    end_date
FROM class_schedule
LIMIT 10;