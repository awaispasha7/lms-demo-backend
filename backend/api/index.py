"""
Vercel serverless function entry point for Django
This file handles all requests and routes them through Django
"""
import os
import sys
import traceback
from pathlib import Path
from io import BytesIO

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
os.environ.setdefault('VERCEL', '1')

# Initialize Django - do this at module level
import django
from django.core.wsgi import get_wsgi_application

django.setup()
application = get_wsgi_application()

# Vercel handler function
# Vercel Python runtime expects handler(req) that returns a dict
def handler(req):
    """
    Handle Vercel serverless requests
    Vercel Python runtime provides req as a dict with method, path, headers, body, query
    """
    try:
        from urllib.parse import urlencode
        
        # Extract request data - Vercel provides req as dict
        method = req.get('method', 'GET') if isinstance(req, dict) else getattr(req, 'method', 'GET')
        path = req.get('path', '/') if isinstance(req, dict) else getattr(req, 'path', '/')
        headers = req.get('headers', {}) if isinstance(req, dict) else getattr(req, 'headers', {})
        body = req.get('body', b'') if isinstance(req, dict) else getattr(req, 'body', b'')
        query = req.get('query', {}) if isinstance(req, dict) else getattr(req, 'query', {})
        
        # Normalize headers to dict
        if not isinstance(headers, dict):
            try:
                headers = dict(headers) if hasattr(headers, 'items') else {}
            except:
                headers = {}
        
        # Build query string
        if isinstance(query, dict):
            query_string = urlencode(query) if query else ''
        else:
            query_string = str(query) if query else ''
        
        # Normalize body
        if isinstance(body, str):
            body = body.encode('utf-8')
        elif body is None:
            body = b''
        
        # Get host from headers
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
        
        # Add all headers to environ (WSGI format)
        for key, value in headers.items():
            # Skip Content-Type and Content-Length (already set)
            if key.lower() in ('content-type', 'content-length'):
                continue
            environ_key = f'HTTP_{key.upper().replace("-", "_")}'
            environ[environ_key] = str(value)
        
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
        
        # Close response if it has close method
        if hasattr(response, 'close'):
            response.close()
        
        # Build response dict
        headers_dict = {header: value for header, value in response_headers}
        body = b''.join(response_body)
        
        # Return dict format (Vercel Python runtime format)
        return {
            'statusCode': status_code,
            'headers': headers_dict,
            'body': body.decode('utf-8') if isinstance(body, bytes) else str(body)
        }
        
    except Exception as e:
        error_trace = traceback.format_exc()
        error_msg = f"Handler error: {str(e)}\n\nTraceback:\n{error_trace}"
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': error_msg
        }
