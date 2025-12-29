# Vercel Deployment Fix

## Issue
The build completes but the handler format might not be compatible with Vercel's Python runtime.

## Solution
The `api/index.py` handler has been updated to work with Vercel's Python runtime. However, if you still encounter issues, try these alternatives:

### Option 1: Use the updated handler (current)
The handler now expects a `req` object with `method`, `path`, `headers`, and `body` attributes.

### Option 2: If Option 1 doesn't work, try this alternative format:

Create a new `api/index.py` with:

```python
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
os.environ.setdefault('VERCEL', '1')

import django
from django.core.wsgi import get_wsgi_application

django.setup()
application = get_wsgi_application()

def handler(request):
    from io import BytesIO
    from urllib.parse import urlencode
    
    # Extract request data
    method = request.get('method', 'GET')
    path = request.get('path', '/')
    headers = request.get('headers', {})
    body = request.get('body', b'')
    query = request.get('query', {})
    
    if isinstance(body, str):
        body = body.encode('utf-8')
    
    query_string = urlencode(query) if query else ''
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.input': BytesIO(body),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'SERVER_NAME': headers.get('host', ''),
        'SERVER_PORT': '443',
        'HTTP_HOST': headers.get('host', ''),
    }
    
    # Add headers
    for key, value in headers.items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # Process request
    status_code = 200
    response_headers = []
    response_body = []
    
    def start_response(status, headers):
        nonlocal status_code, response_headers
        status_code = int(status.split()[0])
        response_headers = headers
    
    response = application(environ, start_response)
    
    for chunk in response:
        response_body.append(chunk)
    
    body = b''.join(response_body)
    
    return {
        'statusCode': status_code,
        'headers': dict(response_headers),
        'body': body.decode('utf-8') if isinstance(body, bytes) else str(body)
    }
```

### Environment Variables Required in Vercel:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False` for production
- `DATABASE_URL` - Your Supabase connection string
- `USE_SUPABASE` - Set to `True`
- `ALLOWED_HOSTS` - Include your Vercel domain

### Static Files
Make sure `STATIC_ROOT` is set in settings.py and run `collectstatic` during build, or configure Vercel to serve static files.

