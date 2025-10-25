-- ============================================
-- Fix year column values
-- ============================================

-- Update all records to have year = 2024
UPDATE class_schedule 
SET year = 2024
WHERE year = 2 OR year IS NULL OR year < 1000;

-- Verify the fix
SELECT 
    'After fix' as status,
    year,
    COUNT(*) as count
FROM class_schedule
GROUP BY year;

-- Sample records to verify
SELECT 
    class_schedule_id,
    semester,
    year,
    start_date,
    end_date
FROM class_schedule
LIMIT 10;