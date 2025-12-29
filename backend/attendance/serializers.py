from rest_framework import serializers
from .models import Attendance, AttendanceReport


class AttendanceSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    marked_by_username = serializers.CharField(source='marked_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'student_username', 'student_email',
            'class_obj', 'class_name', 'date', 'status',
            'marked_by', 'marked_by_username', 'marked_at',
            'latitude', 'longitude', 'remarks', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'marked_at', 'created_at', 'updated_at']


class AttendanceReportSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    
    class Meta:
        model = AttendanceReport
        fields = [
            'id', 'student', 'student_username', 'student_email',
            'class_obj', 'class_name', 'start_date', 'end_date',
            'total_days', 'present_days', 'absent_days', 'late_days',
            'excused_days', 'attendance_percentage', 'generated_at',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_days', 'present_days', 'absent_days',
            'late_days', 'excused_days', 'attendance_percentage',
            'generated_at', 'created_at', 'updated_at'
        ]

