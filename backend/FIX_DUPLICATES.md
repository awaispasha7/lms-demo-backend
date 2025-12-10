# Fix Duplicate Assignments Issue

## Problem
- Teacher portal shows many duplicate assignments
- Student portal shows nothing
- Seed function is running on every serverless invocation, creating duplicates

## Solution

### Step 1: Disable Seed Function ✅
The seed function has been disabled in `server.js`. It will no longer run automatically.

### Step 2: Clean Up Duplicates

1. Go to Supabase Dashboard → SQL Editor
2. Run `CLEANUP_DUPLICATES.sql`:
   ```sql
   DELETE FROM assignments;
   ```
   This will delete ALL assignments (you'll re-insert them next)

### Step 3: Insert Fresh Assignments

1. Still in Supabase SQL Editor
2. Run `insert_sample_assignments.sql` to insert all 12 assignments

### Step 4: Redeploy Backend

After cleaning up and inserting, redeploy your backend to Vercel.

## Why This Happened

On Vercel serverless:
- Each function invocation can be a new instance
- The seed function was running on every start
- The check for existing assignments might have failed due to timing
- This created duplicates on every cold start

## Prevention

The seed function is now disabled. Always insert assignments via SQL in Supabase, not through the seed function.

## Verify

After cleanup:
- Teacher portal should show exactly 12 unique assignments
- Student portal should show the same 12 assignments
- No duplicates

