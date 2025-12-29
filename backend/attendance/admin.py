from django.contrib import admin
from .models import Attendance, AttendanceReport


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'class_obj', 'date', 'status', 'marked_by', 'marked_at']
    list_filter = ['status', 'date', 'class_obj']
    search_fields = ['student__username', 'class_obj__name']


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'class_obj', 'start_date', 'end_date', 'attendance_percentage', 'generated_at']
    list_filter = ['start_date', 'end_date']
    search_fields = ['student__username', 'class_obj__name']

