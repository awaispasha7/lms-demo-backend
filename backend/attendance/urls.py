from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, AttendanceReportViewSet

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'attendance-reports', AttendanceReportViewSet, basename='attendance-reports')

urlpatterns = [
    path('', include(router.urls)),
]

