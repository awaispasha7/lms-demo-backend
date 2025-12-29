from django.contrib import admin
from .models import School, AcademicYear, Subject, Class, StudentClass, TeacherSubjectClass


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date', 'school']
    search_fields = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'school', 'created_at']
    list_filter = ['school', 'is_active']
    search_fields = ['name', 'code']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'academic_year', 'grade_level', 'class_teacher']
    list_filter = ['academic_year', 'grade_level', 'is_active']
    search_fields = ['name', 'code']


@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'class_obj', 'academic_year', 'enrollment_date', 'is_active']
    list_filter = ['academic_year', 'is_active']
    search_fields = ['student__username', 'class_obj__name']


@admin.register(TeacherSubjectClass)
class TeacherSubjectClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'subject', 'class_obj', 'academic_year', 'is_active']
    list_filter = ['academic_year', 'is_active']
    search_fields = ['teacher__username', 'subject__name', 'class_obj__name']
