"""
Context processors for Django templates
"""
from django.conf import settings

def backend_api_url(request):
    """
    Add BACKEND_API_URL to all template contexts
    """
    return {
        'BACKEND_API_URL': getattr(settings, 'BACKEND_API_URL', '')
    }

