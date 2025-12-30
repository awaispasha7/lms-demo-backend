"""
URL configuration for lms_backend project.
Frontend-only: All data comes from client's backend API.
"""
from django.contrib import admin
from django.urls import path
from assignments import views as assignment_views

urlpatterns = [
    # Admin (optional, for Django admin if needed)
    path('admin/', admin.site.urls),
    
    # Frontend pages only - all data comes from client's backend API
    path('', assignment_views.index, name='index'),
    path('test-backend-url', assignment_views.test_backend_url, name='test_backend_url'),
    path('teacher', assignment_views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/assignments/list', assignment_views.teacher_assignment_list, name='teacher_assignment_list'),
    path('teacher/assignments/create', assignment_views.teacher_assignment_create, name='teacher_assignment_create'),
    path('teacher/assignments/<int:assignment_id>', assignment_views.teacher_assignment_detail, name='teacher_assignment_detail'),
    path('teacher/submissions/<int:submission_id>', assignment_views.teacher_submission_detail, name='teacher_submission_detail'),
    path('student', assignment_views.student_dashboard, name='student_dashboard'),
    path('student/assignments/<int:assignment_id>', assignment_views.student_assignment_detail, name='student_assignment_detail'),
]
