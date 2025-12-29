from django.contrib import admin
from .models import Assignment, Submission, Grade


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'teacher', 'class_obj', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'teacher']
    search_fields = ['title', 'description']
    raw_id_fields = ['teacher', 'class_obj', 'subject']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assignment', 'student', 'student_name', 'status', 'submitted_at']
    list_filter = ['status', 'submitted_at']
    search_fields = ['student_name', 'student__username', 'assignment__title']
    raw_id_fields = ['assignment', 'student']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'submission', 'score', 'max_score', 'percentage', 'graded_by', 'graded_at']
    list_filter = ['graded_at', 'graded_by']
    search_fields = ['submission__student__username', 'submission__assignment__title']
    raw_id_fields = ['submission', 'graded_by']
    readonly_fields = ['percentage']
