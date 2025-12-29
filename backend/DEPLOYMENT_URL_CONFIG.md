# Deployment URL Configuration

## Reference API URL

The client provided reference API: `http://3.226.252.253:8000/`

This was the **reference API** we matched. Your Django app should **replace** this.

## Options

### Option 1: Deploy Django to Same Server (Recommended)

**Replace the old Express.js backend** with your Django app on the same server:

1. **Deploy Django to `3.226.252.253:8000`**
   - This replaces the old backend
   - Same URL, new Django backend
   - Frontend doesn't need changes

2. **Update `.env` for production:**
   ```env
   ALLOWED_HOSTS=3.226.252.253,localhost,127.0.0.1
   DEBUG=False
   USE_SUPABASE=True
   # ... (Supabase credentials)
   ```

3. **Run Django on port 8000:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   # Or with gunicorn:
   gunicorn -c gunicorn_config.py lms_backend.wsgi --bind 0.0.0.0:8000
   ```

### Option 2: Deploy to New Server

If deploying to a different server (like Vercel):

1. **Deploy Django to new URL** (e.g., `your-app.vercel.app`)
2. **Update frontend** to point to new URL
3. **Update CORS** settings to allow new origin

## Current Configuration

I've updated `settings.py` to include `3.226.252.253` in:
- ✅ `ALLOWED_HOSTS` - Allows requests to that domain
- ✅ `CORS_ALLOWED_ORIGINS` - Allows CORS from that domain

## To Deploy to Same Server

1. **SSH to server** `3.226.252.253`
2. **Stop old Express.js backend**
3. **Deploy Django app**
4. **Run on port 8000:**
   ```bash
   gunicorn -c gunicorn_config.py lms_backend.wsgi --bind 0.0.0.0:8000
   ```

## Important Notes

- ✅ Django app **replaces** the old Express.js backend
- ✅ Same URL (`3.226.252.253:8000`) = Same API structure
- ✅ All endpoints match the reference API
- ✅ Frontend can use same URL (no changes needed)

## Summary

**Yes, you should use the same URL** if you're replacing the old backend on that server. The Django app is designed to match that API exactly!

