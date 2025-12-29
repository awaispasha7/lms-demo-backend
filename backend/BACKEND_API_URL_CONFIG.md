# Backend API URL Configuration

## Overview
The Django full-stack application is configured to use the client's backend URL (`http://3.226.252.253:8000/`) for all API calls from the frontend templates.

## Configuration

### Settings
In `lms_backend/settings.py`:
```python
BACKEND_API_URL = config('BACKEND_API_URL', default='http://3.226.252.253:8000')
```

### How It Works

1. **Context Processor**: The `BACKEND_API_URL` is automatically added to all template contexts via `lms_backend/context_processors.py`

2. **Base Template**: The `base.html` template includes:
   - `window.BACKEND_API_URL` JavaScript variable
   - HTMX configuration to automatically prepend the backend URL to all `/api/` requests

3. **Fetch Calls**: All `fetch()` calls in templates use:
   ```javascript
   const apiUrl = window.BACKEND_API_URL || '';
   const response = await fetch(`${apiUrl}/api/...`, {...});
   ```

4. **HTMX Attributes**: All `hx-post="/api/..."` and `hx-get="/api/..."` attributes are automatically rewritten to use the backend URL via the HTMX event listener.

## Environment Variables

To override the backend URL, set in Vercel or `.env`:
```
BACKEND_API_URL=http://3.226.252.253:8000
```

## Local Development

- If `BACKEND_API_URL` is not set, API calls will use relative paths (same server)
- If set, all API calls will go to the specified backend URL

## Notes

- Template rendering still happens on the current server (Vercel or local)
- Only API calls (fetch/HTMX) are redirected to the backend URL
- This allows the frontend to be served from Vercel while API calls go to the client's backend

