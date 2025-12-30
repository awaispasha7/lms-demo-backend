# Frontend-only views - All data comes from client's backend API
from django.shortcuts import render

# ============================================
# TEMPLATE VIEWS (Django + HTMX)
# All data fetching happens in templates via JavaScript/HTMX
# calling the client's backend API at BACKEND_API_URL
# ============================================

def index(request):
    """Home page"""
    return render(request, 'assignments/index.html')


def teacher_dashboard(request):
    """Teacher dashboard - Frontend only, data comes from client's API"""
    # No database queries - templates will fetch data via API
    return render(request, 'assignments/teacher/dashboard.html')


def teacher_assignment_list(request):
    """Teacher assignment list - Frontend only, data comes from client's API"""
    # No database queries - templates will fetch data via API
    return render(request, 'assignments/teacher/assignment_list.html')


def teacher_assignment_create(request):
    """Create new assignment - Frontend only, form submits to client's API"""
    # No database operations - form submits to client's backend API
    return render(request, 'assignments/teacher/create.html')


def teacher_assignment_detail(request, assignment_id):
    """Assignment detail - Frontend only, data comes from client's API"""
    # No database queries - templates will fetch data via API using assignment_id
    context = {'assignment_id': assignment_id}
    return render(request, 'assignments/teacher/assignment_detail.html', context)


def teacher_submission_detail(request, submission_id):
    """Submission detail - Frontend only, data comes from client's API"""
    # No database queries - templates will fetch data via API using submission_id
    context = {'submission_id': submission_id}
    return render(request, 'assignments/teacher/submission_detail.html', context)


def student_dashboard(request):
    """Student dashboard - Frontend only, data comes from client's API"""
    # No database queries - templates will fetch data via API
    return render(request, 'assignments/student/dashboard.html')


def student_assignment_detail(request, assignment_id):
    """Student assignment detail - Frontend only, data comes from client's API"""
    # No database queries - templates will fetch data via API using assignment_id
    context = {'assignment_id': assignment_id}
    return render(request, 'assignments/student/assignment_detail.html', context)


def test_backend_url(request):
    """Test page to verify backend API URL configuration"""
    from django.conf import settings
    context = {
        'BACKEND_API_URL': getattr(settings, 'BACKEND_API_URL', '')
    }
    return render(request, 'assignments/test_backend_url.html', context)
