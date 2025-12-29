"""
Vercel serverless function entry point for Django
This file handles all requests and routes them through Django
"""
import os
import sys
from pathlib import Path
from io import BytesIO

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
os.environ.setdefault('VERCEL', '1')

# Initialize Django
import django
from django.core.wsgi import get_wsgi_application

django.setup()
application = get_wsgi_application()

# Vercel handler function
def handler(req):
    """
    Handle Vercel serverless requests
    Vercel Python runtime may provide req as dict or object
    """
    from urllib.parse import urlencode
    
    # Handle both dict and object formats
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
    
    # Build query string
    query_string = urlencode(query) if query else ''
    
    if isinstance(body, str):
        body = body.encode('utf-8')
    
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
    
    # Add all headers to environ
    for key, value in headers.items():
        environ_key = f'HTTP_{key.upper().replace("-", "_")}'
        environ[environ_key] = value
    
    # Response status and headers
    status_code = 200
    response_headers = []
    response_body = []
    
    def start_response(status, headers):
        nonlocal status_code, response_headers
        status_code = int(status.split()[0])
        response_headers = headers
    
    # Process through Django WSGI application
    response = application(environ, start_response)
    
    # Collect response body
    for chunk in response:
        response_body.append(chunk)
    
    # Build response dict
    headers_dict = {header: value for header, value in response_headers}
    body = b''.join(response_body)
    
    return {
        'statusCode': status_code,
        'headers': headers_dict,
        'body': body.decode('utf-8') if isinstance(body, bytes) else str(body)
    }
