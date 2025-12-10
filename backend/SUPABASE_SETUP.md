# Supabase Setup Instructions

## Step 1: Create Tables in Supabase

1. Go to your Supabase project: https://supabase.com/dashboard
2. Click on "SQL Editor" in the left sidebar
3. Open the file `supabase_schema.sql` from this directory
4. Copy and paste the entire SQL into the SQL Editor
5. Click "Run" to execute the SQL
6. Verify tables were created by going to "Table Editor" - you should see `assignments` and `submissions` tables

## Step 2: Add Environment Variables

In your Vercel backend project, add these environment variables:

- `SUPABASE_URL`: `https://yntmdbalhjgmiyfauaui.supabase.co`
- `SUPABASE_KEY`: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InludG1kYmFsaGpnbWl5ZmF1YXVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUzODIxNjYsImV4cCI6MjA4MDk1ODE2Nn0.xM8gJ0eiiN2hNqcVNYOfCDv3nqQGA5pwGkAmpa1-Mv0`

Or if you prefer to use environment variables (recommended):
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon/public key

## Step 3: Install Dependencies

```bash
cd backend
pnpm install
```

This will install `@supabase/supabase-js`.

## Step 4: Deploy

After updating the code, redeploy your backend to Vercel.

## How It Works

- All assignments and submissions are now stored in Supabase PostgreSQL database
- Data persists across serverless cold starts
- The seed function will only run once (checks if assignments exist)
- All CRUD operations use Supabase queries

## Benefits

✅ Persistent storage - data never disappears
✅ Real-time capabilities available (can be added later)
✅ Scalable PostgreSQL database
✅ Free tier available
✅ Better than in-memory storage for production

