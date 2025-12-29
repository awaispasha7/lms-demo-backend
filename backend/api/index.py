"""
Vercel serverless function entry point for Django
This file handles all requests and routes them through Django
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

# Initialize Django
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

django.setup()
application = get_wsgi_application()

# Vercel handler function
def handler(request):
    """
    Handle Vercel serverless requests
    """
    from django.http import HttpRequest, HttpResponse
    from django.core.handlers.wsgi import WSGIRequest
    from django.utils.encoding import force_str
    import io
    
    # Convert Vercel request to Django WSGI request
    environ = {
        'REQUEST_METHOD': request.get('method', 'GET'),
        'PATH_INFO': request.get('path', '/'),
        'QUERY_STRING': request.get('query', {}),
        'CONTENT_TYPE': request.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': str(len(request.get('body', ''))),
        'wsgi.input': io.BytesIO(request.get('body', b'').encode() if isinstance(request.get('body'), str) else request.get('body', b'')),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'SERVER_NAME': request.get('headers', {}).get('host', ''),
        'SERVER_PORT': '443',
        'HTTP_HOST': request.get('headers', {}).get('host', ''),
    }
    
    # Add headers to environ
    for key, value in request.get('headers', {}).items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # Create WSGI request
    wsgi_request = WSGIRequest(environ)
    
    # Process through Django
    response = application(environ, lambda status, headers: None)
    
    # Extract response
    status_code = response.status_code if hasattr(response, 'status_code') else 200
    headers = dict(response.headers) if hasattr(response, 'headers') else {}
    content = b''.join(response) if hasattr(response, '__iter__') else str(response).encode()
    
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': content.decode('utf-8') if isinstance(content, bytes) else str(content)
    }
