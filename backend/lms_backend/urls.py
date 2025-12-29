"""
URL configuration for lms_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from assignments import views as assignment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/academics/', include('academics.urls')),
    path('api/assignments/', include('assignments.urls')),  # API endpoints only
    path('api/attendance/', include('attendance.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/policies/', include('policies.urls')),
    path('api/ai/', include('ai.urls')),
    
    # Template views at root level
    path('', assignment_views.index, name='index'),
    path('teacher', assignment_views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/assignments/list', assignment_views.teacher_assignment_list, name='teacher_assignment_list'),
    path('teacher/assignments/create', assignment_views.teacher_assignment_create, name='teacher_assignment_create'),
    path('teacher/assignments/<int:assignment_id>', assignment_views.teacher_assignment_detail, name='teacher_assignment_detail'),
    path('teacher/submissions/<int:submission_id>', assignment_views.teacher_submission_detail, name='teacher_submission_detail'),
    path('student', assignment_views.student_dashboard, name='student_dashboard'),
    path('student/assignments/<int:assignment_id>', assignment_views.student_assignment_detail, name='student_assignment_detail'),
]
