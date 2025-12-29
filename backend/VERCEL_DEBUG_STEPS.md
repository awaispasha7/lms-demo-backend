# Vercel Debugging Steps

## Current Issue
Function is crashing with `500: INTERNAL_SERVER_ERROR` and `FUNCTION_INVOCATION_FAILED`

## Step 1: Check Vercel Function Logs (MOST IMPORTANT)

1. Go to **Vercel Dashboard** → Your Project
2. Click on **Deployments** tab
3. Click on the **latest deployment** (the one that's failing)
4. Click on the **"Logs"** tab (or "Function Logs")
5. Look for error messages - they will show the actual Python exception

**What to look for:**
- `ModuleNotFoundError` - Missing package
- `ImproperlyConfigured` - Django settings issue
- `Database connection` errors
- Any Python traceback

**Copy the full error message and share it!**

## Step 2: Check Environment Variables

1. Go to **Vercel Dashboard** → Your Project → **Settings**
2. Click **Environment Variables**
3. Verify these are set:
   - ✅ `SECRET_KEY` - Must be set!
   - ✅ `DATABASE_URL` - Your Supabase connection string
   - ✅ `USE_SUPABASE` - Set to `True`
   - ✅ `DEBUG` - Set to `False` for production
   - ✅ `BACKEND_API_URL` - Set to `http://3.226.252.253:8000`
   - ✅ `ALLOWED_HOSTS` - Include your Vercel domain

## Step 3: Test Simple Handler (Optional)

If you want to test if the handler format works, temporarily change `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/test.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/test.py"
    }
  ]
}
```

This uses a simple test handler. If this works, the issue is with Django initialization.

## Step 4: Common Issues & Fixes

### Issue: ModuleNotFoundError
**Fix:** Add missing package to `requirements.txt`

### Issue: SECRET_KEY not set
**Fix:** Add `SECRET_KEY` environment variable in Vercel

### Issue: Database connection failed
**Fix:** 
- Check `DATABASE_URL` is correct
- Verify Supabase allows connections from Vercel IPs
- Check `USE_SUPABASE=True` is set

### Issue: Django settings error
**Fix:** Check `settings.py` for any hardcoded paths or missing config

### Issue: Handler format wrong
**Fix:** The handler format might need adjustment based on Vercel's Python runtime version

## Step 5: Enable Debug Mode Temporarily

In Vercel Environment Variables, temporarily set:
```
DEBUG=True
```

This will show more detailed error pages (but don't leave it on in production!)

## What to Share

When asking for help, share:
1. ✅ **Full error from Vercel Function Logs** (most important!)
2. ✅ List of environment variables you've set
3. ✅ Any build errors from Vercel build logs
4. ✅ Python version (should be 3.11 or 3.12)

## Next Steps

1. **Check the logs first** - This will tell us exactly what's wrong
2. **Share the error** - I can help fix it once we see the actual error
3. **Verify env vars** - Make sure all required variables are set

The handler now includes logging, so errors should appear in Vercel logs even if they don't show in the response.

