-- Clean up duplicate assignments in Supabase
-- Run this BEFORE inserting the new assignments

-- Option 1: Delete ALL assignments and start fresh (Recommended)
DELETE FROM assignments;

-- Option 2: Keep only unique assignments by title (if you want to preserve some)
-- This keeps the first occurrence of each unique title
-- DELETE FROM assignments
-- WHERE id NOT IN (
--   SELECT MIN(id)
--   FROM assignments
--   GROUP BY title
-- );

-- Verify cleanup
SELECT COUNT(*) as total_assignments FROM assignments;

