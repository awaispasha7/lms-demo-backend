from rest_framework import serializers
from .models import AcademicYear, Subject, Class, School, StudentClass, TeacherSubjectClass


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'id', 'name', 'code', 'address', 'phone', 'email', 'website',
            'established_year', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AcademicYearSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = AcademicYear
        fields = [
            'id', 'school', 'school_name', 'name', 'start_date', 'end_date',
            'is_current', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubjectSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = Subject
        fields = [
            'id', 'school', 'school_name', 'name', 'code', 'description',
            'credit_hours', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClassSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    class_teacher_username = serializers.CharField(source='class_teacher.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Class
        fields = [
            'id', 'school', 'school_name', 'academic_year', 'academic_year_name',
            'name', 'code', 'grade_level', 'capacity', 'class_teacher',
            'class_teacher_username', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentClassSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    
    class Meta:
        model = StudentClass
        fields = [
            'id', 'student', 'student_username', 'student_email',
            'class_obj', 'class_name', 'academic_year', 'academic_year_name',
            'enrollment_date', 'roll_number', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'enrollment_date', 'created_at', 'updated_at']


class TeacherSubjectClassSerializer(serializers.ModelSerializer):
    teacher_username = serializers.CharField(source='teacher.username', read_only=True)
    teacher_email = serializers.EmailField(source='teacher.email', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    
    class Meta:
        model = TeacherSubjectClass
        fields = [
            'id', 'teacher', 'teacher_username', 'teacher_email',
            'subject', 'subject_name', 'class_obj', 'class_name',
            'academic_year', 'academic_year_name', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
