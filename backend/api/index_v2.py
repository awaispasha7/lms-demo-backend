"""
Vercel handler - Alternative approach using WSGI application directly
Based on Vercel's expected format for Django
"""
import os
import sys
from pathlib import Path

# Setup
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
os.environ.setdefault('VERCEL', '1')

# Import WSGI application directly (like Flask example)
from lms_backend.wsgi import application as django_app

# Vercel handler that wraps WSGI
def handler(req):
    """Vercel handler wrapping Django WSGI"""
    from io import BytesIO
    from urllib.parse import urlencode
    
    # Extract request
    if isinstance(req, dict):
        method = req.get('method', 'GET')
        path = req.get('path', '/')
        headers = req.get('headers', {})
        body = req.get('body', b'')
        query = req.get('query', {})
    else:
        method = getattr(req, 'method', 'GET')
        path = getattr(req, 'path', '/')
        headers = getattr(req, 'headers', {})
        body = getattr(req, 'body', b'')
        query = getattr(req, 'query', {})
    
    # Normalize
    if isinstance(body, str):
        body = body.encode('utf-8')
    if not isinstance(headers, dict):
        headers = {}
    if isinstance(query, dict):
        query_string = urlencode(query) if query else ''
    else:
        query_string = ''
    
    host = headers.get('host', headers.get('Host', ''))
    
    # WSGI environ
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
    
    # Process
    status_code = 200
    response_headers = []
    response_body = []
    
    def start_response(status, headers):
        nonlocal status_code, response_headers
        status_code = int(status.split()[0])
        response_headers = headers
    
    response = django_app(environ, start_response)
    
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

