"""
Minimal Vercel handler - try this if index.py doesn't work
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
os.environ.setdefault('VERCEL', '1')

# Import Django
import django
from django.core.wsgi import get_wsgi_application
from io import BytesIO

# Initialize Django
django.setup()
application = get_wsgi_application()

def handler(req):
    """Vercel handler - minimal version"""
    from urllib.parse import urlencode
    
    # Get request data
    method = req.get('method', 'GET') if isinstance(req, dict) else 'GET'
    path = req.get('path', '/') if isinstance(req, dict) else '/'
    headers = req.get('headers', {}) if isinstance(req, dict) else {}
    body = req.get('body', b'') if isinstance(req, dict) else b''
    query = req.get('query', {}) if isinstance(req, dict) else {}
    
    # Normalize
    if isinstance(body, str):
        body = body.encode('utf-8')
    if isinstance(headers, dict):
        pass
    else:
        headers = {}
    if isinstance(query, dict):
        query_string = urlencode(query) if query else ''
    else:
        query_string = ''
    
    host = headers.get('host', headers.get('Host', ''))
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('content-type', headers.get('Content-Type', '')),
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.input': BytesIO(body),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'SERVER_NAME': host,
        'SERVER_PORT': '443',
        'HTTP_HOST': host,
    }
    
    # Add headers
    for key, value in headers.items():
        if key.lower() not in ('content-type', 'content-length'):
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = str(value)
    
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
    
    if hasattr(response, 'close'):
        response.close()
    
    body = b''.join(response_body)
    
    return {
        'statusCode': status_code,
        'headers': dict(response_headers),
        'body': body.decode('utf-8') if isinstance(body, bytes) else str(body)
    }

