from rest_framework import serializers
from .models import Assignment, Submission, Grade


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for Assignment matching API structure"""
    teacher_username = serializers.CharField(source='teacher.username', read_only=True)
    teacher_email = serializers.EmailField(source='teacher.email', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    submission_count = serializers.SerializerMethodField()
    graded_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'teacher', 'teacher_username', 'teacher_email',
            'class_obj', 'class_name', 'subject', 'subject_name', 'due_date',
            'max_score', 'status', 'instructions', 'questions', 'submission_count',
            'graded_count', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_submission_count(self, obj):
        """Get submission count from annotation or calculate"""
        if hasattr(obj, 'total_submissions'):
            return obj.total_submissions
        return obj.submissions.count()
    
    def get_graded_count(self, obj):
        """Get graded count from annotation or calculate"""
        if hasattr(obj, 'graded_count'):
            return obj.graded_count
        return obj.submissions.filter(status='GRADED').count()


class AssignmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Assignment"""
    
    class Meta:
        model = Assignment
        fields = [
            'title', 'description', 'teacher', 'class_obj', 'subject',
            'due_date', 'max_score', 'status', 'instructions', 'questions'
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for Submission matching API structure"""
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True, allow_null=True)
    student_email = serializers.EmailField(source='student.email', read_only=True, allow_null=True)
    grade = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'assignment_title', 'student', 'student_username',
            'student_email', 'submission_text', 'status', 'submitted_at',
            'is_active', 'created_at', 'updated_at', 'grade'
        ]
        read_only_fields = ['id', 'submitted_at', 'created_at', 'updated_at']
    
    def get_grade(self, obj):
        if hasattr(obj, 'grade'):
            return GradeSerializer(obj.grade).data
        return None


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Submission"""
    
    class Meta:
        model = Submission
        fields = ['assignment', 'student', 'submission_text', 'status']


class GradeSerializer(serializers.ModelSerializer):
    """Serializer for Grade matching API structure"""
    submission_details = SubmissionSerializer(source='submission', read_only=True)
    graded_by_username = serializers.CharField(source='graded_by.username', read_only=True, allow_null=True)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = Grade
        fields = [
            'id', 'submission', 'submission_details', 'score', 'max_score',
            'percentage', 'feedback', 'graded_by', 'graded_by_username',
            'graded_at', 'ai_suggested_score', 'ai_suggested_feedback',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'graded_at', 'created_at', 'updated_at', 'percentage']


class GradeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Grade"""
    
    class Meta:
        model = Grade
        fields = ['submission', 'score', 'max_score', 'feedback', 'graded_by', 'ai_suggested_score', 'ai_suggested_feedback']
