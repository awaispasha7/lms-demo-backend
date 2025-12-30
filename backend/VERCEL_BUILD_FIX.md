# Vercel Build Fix

## Error Fixed

**Error:** `Cannot read properties of undefined (reading 'fsPath')`

**Cause:** Missing `builds` section in `vercel.json`

**Fix:** Added `builds` section to specify Python handler

## Updated `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

## Changes Made

1. ✅ Added `builds` section - Tells Vercel to build `api/index.py` as a Python function
2. ✅ Cleaned up `requirements.txt` - Removed unused packages (REST Framework, PostgreSQL, etc.)
3. ✅ Kept only essential packages for frontend-only app

## Minimal Requirements

Since we're frontend-only, we only need:
- `Django` - Core framework
- `python-decouple` - Environment variables
- `django-cors-headers` - CORS support
- `whitenoise` - Static files serving

## Next Steps

1. **Commit and push** the updated `vercel.json` and `requirements.txt`
2. **Redeploy** on Vercel
3. **Check build logs** - Should now build successfully
4. **Test pages** - Visit your Vercel URL to verify frontend loads

## Environment Variables Needed

Make sure these are set in Vercel:
```
SECRET_KEY=your-django-secret-key
DEBUG=False
BACKEND_API_URL=http://3.226.252.253:8000
```

**Note:** No database variables needed since we're frontend-only!

