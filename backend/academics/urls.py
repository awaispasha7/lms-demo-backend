from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SchoolViewSet, AcademicYearViewSet, SubjectViewSet,
    ClassViewSet, StudentClassViewSet, TeacherSubjectClassViewSet
)

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='schools')
router.register(r'academic-years', AcademicYearViewSet, basename='academic-years')
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'classes', ClassViewSet, basename='classes')
router.register(r'student-enrollments', StudentClassViewSet, basename='student-enrollments')
router.register(r'teacher-assignments', TeacherSubjectClassViewSet, basename='teacher-assignments')

urlpatterns = [
    path('', include(router.urls)),
]
