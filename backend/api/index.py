"""
Vercel serverless function entry point for Django
This file handles all requests and routes them through Django
"""
import os
import sys
import traceback
from pathlib import Path
from io import BytesIO

# Catch any module-level errors
_module_error = None
try:
    # Add project root to Python path
    BASE_DIR = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(BASE_DIR))

    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
    os.environ.setdefault('VERCEL', '1')
except Exception as e:
    _module_error = f"Module initialization error: {str(e)}\n\n{traceback.format_exc()}"

# Lazy Django initialization
application = None
django_error = None

def get_application():
    """Lazy initialization of Django application"""
    global application, django_error
    if application is not None:
        return application
    
    try:
        import django
        from django.core.wsgi import get_wsgi_application
        
        django.setup()
        application = get_wsgi_application()
        return application
    except Exception as e:
        django_error = str(e)
        import traceback
        django_error += "\n\n" + traceback.format_exc()
        return None

# Vercel handler - must be a callable at module level
# The handler function will be called by Vercel's runtime
def _handle_request(req):
    """
    Internal request handler - processes the actual request
    """
    # Check for module-level errors first
    if _module_error:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': f"Module initialization error:\n\n{_module_error}"
        }
    
    try:
        # Initialize Django application (lazy)
        app = get_application()
        if app is None:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain; charset=utf-8'},
                'body': f"Django initialization failed:\n\n{django_error}"
            }
        
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
        response = app(environ, start_response)
        
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
        
        # Log to Vercel logs
        print(f"Handler exception: {error_msg}")
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': error_msg
        }

# Export handler function - Vercel Python runtime expects this
# Make it a simple function at module level
def handler(req):
    """Vercel serverless function handler"""
    return _handle_request(req)
