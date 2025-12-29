"""
Vercel serverless function entry point for Django
Ultra-minimal structure - only handler function at module level
"""
import os
import sys
from pathlib import Path

# Minimal setup - no Django imports at module level
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
os.environ.setdefault('VERCEL', '1')

# Global cache for Django app
_app_cache = None

def handler(req):
    """
    Vercel serverless function handler
    Everything happens inside this function to avoid Vercel detection issues
    """
    global _app_cache
    
    try:
        # Lazy Django initialization
        if _app_cache is None:
            import django
            from django.core.wsgi import get_wsgi_application
            django.setup()
            _app_cache = get_wsgi_application()
        
        app = _app_cache
        
        from urllib.parse import urlencode
        from io import BytesIO
        
        # Extract request data
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
        if not isinstance(headers, dict):
            headers = dict(headers) if hasattr(headers, 'items') else {}
        if isinstance(body, str):
            body = body.encode('utf-8')
        elif body is None:
            body = b''
        if isinstance(query, dict):
            query_string = urlencode(query) if query else ''
        else:
            query_string = str(query) if query else ''
        
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
        
        response = app(environ, start_response)
        
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
        
    except Exception as e:
        import traceback
        error_msg = f"Handler error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(error_msg)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': error_msg
        }
