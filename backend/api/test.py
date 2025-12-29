"""
Simple test handler to verify Vercel Python runtime works
"""
def handler(req):
    """Simple test handler"""
    try:
        # Try to get request info
        if isinstance(req, dict):
            method = req.get('method', 'GET')
            path = req.get('path', '/')
        else:
            method = getattr(req, 'method', 'GET')
            path = getattr(req, 'path', '/')
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': f'''
            <html>
            <head><title>Vercel Test</title></head>
            <body>
                <h1>Vercel Handler Test - SUCCESS!</h1>
                <p>Method: {method}</p>
                <p>Path: {path}</p>
                <p>Request Type: {type(req).__name__}</p>
                <p>Request Content: {str(req)[:200]}</p>
            </body>
            </html>
            '''
        }
    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': f'Test handler error: {str(e)}\n\n{traceback.format_exc()}'
        }

