from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import AssignmentViewSet, SubmissionViewSet, GradeViewSet

# API Router for ViewSets (matching API structure)
router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet, basename='assignments')
router.register(r'submissions', SubmissionViewSet, basename='submissions')
router.register(r'grades', GradeViewSet, basename='grades')

# API URL patterns only (no template views to avoid namespace conflicts)
urlpatterns = [
    # API endpoints via ViewSets (matching /api/assignments/ structure)
    path('', include(router.urls)),
    
    # Legacy function-based views (for backward compatibility)
    path('api/health', views.api_health, name='api_health'),
    path('api/info', views.api_info, name='api_info'),
    path('api/teacher/assignments', views.api_teacher_assignments, name='api_teacher_assignments'),
    path('api/teacher/assignments/<int:assignment_id>', views.api_teacher_assignment_detail, name='api_teacher_assignment_detail'),
    path('api/teacher/assignments/<int:assignment_id>/submissions', views.api_teacher_submissions, name='api_teacher_submissions'),
    path('api/teacher/assignments/<int:assignment_id>/auto-grade', views.api_teacher_auto_grade, name='api_teacher_auto_grade'),
    path('api/teacher/submissions', views.api_teacher_all_submissions, name='api_teacher_all_submissions'),
    path('api/teacher/submissions/<int:submission_id>', views.api_teacher_submission_detail, name='api_teacher_submission_detail'),
    path('api/teacher/submissions/<int:submission_id>/generate-feedback', views.api_teacher_generate_feedback, name='api_teacher_generate_feedback'),
    path('api/teacher/submissions/<int:submission_id>/finalize', views.api_teacher_finalize_grade, name='api_teacher_finalize_grade'),
    path('api/student/assignments', views.api_student_assignments, name='api_student_assignments'),
    path('api/student/assignments/<int:assignment_id>', views.api_student_assignment_detail, name='api_student_assignment_detail'),
    path('api/student/assignments/<int:assignment_id>/submit', views.api_student_submit, name='api_student_submit'),
    path('api/student/submissions', views.api_student_submissions, name='api_student_submissions'),
    path('api/student/submissions/<int:submission_id>', views.api_student_submission_detail, name='api_student_submission_detail'),
    path('api/student/submissions/<int:submission_id>/details', views.api_student_submission_detail, name='api_student_submission_details'),
]
