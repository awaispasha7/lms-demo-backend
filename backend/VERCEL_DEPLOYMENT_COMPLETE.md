# Vercel Deployment - Complete Setup

## Architecture

✅ **Full Django Full-Stack App on Vercel**
- Django templates with HTMX and Tailwind CSS
- All pages rendered server-side on Vercel

✅ **API Calls to Client's Backend**
- All frontend API calls go to `http://3.226.252.253:8000/`
- Configured via `BACKEND_API_URL` setting

## Configuration Summary

### 1. Backend API URL
- **Setting**: `BACKEND_API_URL = http://3.226.252.253:8000`
- **Location**: `lms_backend/settings.py`
- **Usage**: All fetch() and HTMX calls automatically use this URL

### 2. Vercel Handler
- **File**: `api/index.py`
- **Format**: Simplified handler that works with Vercel's Python runtime
- **Error Handling**: Comprehensive error catching with tracebacks

### 3. ALLOWED_HOSTS
- Automatically includes Vercel domains (`*.vercel.app`)
- Also includes: `localhost`, `127.0.0.1`, `3.226.252.253`

## Environment Variables for Vercel

Set these in Vercel Dashboard → Settings → Environment Variables:

```
SECRET_KEY=your-django-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
USE_SUPABASE=True
BACKEND_API_URL=http://3.226.252.253:8000
ALLOWED_HOSTS=your-app.vercel.app,*.vercel.app,3.226.252.253
OPENAI_API_KEY=your-openai-key (if using AI features)
```

## How It Works

1. **User visits Vercel URL** → Django renders template
2. **Template includes JavaScript** → Sets `window.BACKEND_API_URL`
3. **User interacts with page** → HTMX/fetch calls go to `http://3.226.252.253:8000/api/...`
4. **Client's backend processes** → Returns response
5. **Frontend updates** → Using HTMX or JavaScript

## Testing

### Local Testing
1. Start server: `python manage.py runserver 8001`
2. Visit: `http://localhost:8001/test-backend-url`
3. Verify API calls go to `http://3.226.252.253:8000`

### Vercel Testing
1. Deploy to Vercel
2. Visit your Vercel URL
3. Open DevTools → Network tab
4. Verify API calls go to `http://3.226.252.253:8000/api/...`

## Troubleshooting

### If Vercel Function Crashes
1. Check Vercel Function Logs (Dashboard → Deployments → Logs)
2. Look for error messages in the handler
3. Verify all environment variables are set
4. Check `ALLOWED_HOSTS` includes your Vercel domain

### If API Calls Fail
1. Check browser console for CORS errors
2. Verify `BACKEND_API_URL` is set correctly
3. Check that client's backend at `http://3.226.252.253:8000` is accessible
4. Verify CORS is configured on client's backend

### Common Issues
- **ModuleNotFoundError**: Check `requirements.txt` includes all dependencies
- **Database connection**: Verify `DATABASE_URL` is correct
- **Static files**: WhiteNoise handles static files automatically

## Files Modified

1. `api/index.py` - Vercel serverless handler
2. `lms_backend/settings.py` - Added `BACKEND_API_URL` and Vercel domain support
3. `lms_backend/context_processors.py` - Makes API URL available in templates
4. `assignments/templates/assignments/base.html` - HTMX configuration
5. All template files - Updated fetch calls to use backend URL

## Next Steps

1. ✅ Set environment variables in Vercel
2. ✅ Deploy to Vercel
3. ✅ Test the deployment
4. ✅ Verify API calls go to client's backend
5. ✅ Check Vercel logs if any issues

