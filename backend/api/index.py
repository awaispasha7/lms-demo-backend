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

# Initialize Django
try:
    import django
    from django.core.wsgi import get_wsgi_application
    
    django.setup()
    application = get_wsgi_application()
except Exception as e:
    # If Django setup fails, we'll catch it in the handler
    application = None
    django_error = str(e)

# Vercel handler function
def handler(req, res=None):
    """
    Handle Vercel serverless requests
    Vercel Python runtime provides req and optionally res
    """
    try:
        from urllib.parse import urlencode
        
        if application is None:
            error_msg = f"Django setup failed: {django_error}"
            if res:
                res.status(500).send(error_msg)
                return
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain'},
                'body': error_msg
            }
        
        # Handle both dict and object formats for req
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
        if isinstance(query, dict):
            query_string = urlencode(query) if query else ''
        else:
            query_string = str(query) if query else ''
        
        if isinstance(body, str):
            body = body.encode('utf-8')
        elif body is None:
            body = b''
        
        # Build WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': headers.get('content-type', '') if isinstance(headers, dict) else getattr(headers, 'get', lambda k, d: '')(('content-type', ''), ''),
            'CONTENT_LENGTH': str(len(body)),
            'wsgi.input': BytesIO(body),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
            'SERVER_NAME': headers.get('host', '') if isinstance(headers, dict) else getattr(headers, 'get', lambda k, d: '')(('host', ''), ''),
            'SERVER_PORT': '443',
            'HTTP_HOST': headers.get('host', '') if isinstance(headers, dict) else getattr(headers, 'get', lambda k, d: '')(('host', ''), ''),
        }
        
        # Add all headers to environ
        if isinstance(headers, dict):
            for key, value in headers.items():
                environ_key = f'HTTP_{key.upper().replace("-", "_")}'
                environ[environ_key] = str(value)
        else:
            # If headers is an object, try to iterate
            try:
                for key, value in headers.items():
                    environ_key = f'HTTP_{key.upper().replace("-", "_")}'
                    environ[environ_key] = str(value)
            except:
                pass
        
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
        
        # Build response
        headers_dict = {header: value for header, value in response_headers}
        body = b''.join(response_body)
        
        # If res object is provided (newer Vercel format)
        if res:
            res.status(status_code)
            for header, value in headers_dict.items():
                res.set_header(header, value)
            res.send(body.decode('utf-8') if isinstance(body, bytes) else str(body))
            return
        
        # Return dict format (older Vercel format)
        return {
            'statusCode': status_code,
            'headers': headers_dict,
            'body': body.decode('utf-8') if isinstance(body, bytes) else str(body)
        }
        
    except Exception as e:
        error_trace = traceback.format_exc()
        error_msg = f"Handler error: {str(e)}\n\nTraceback:\n{error_trace}"
        
        if res:
            res.status(500).send(error_msg)
            return
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': error_msg
        }
