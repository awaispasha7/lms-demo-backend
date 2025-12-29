from rest_framework import serializers
from .models import Report, ReportTemplate


class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ['id', 'name', 'report_type', 'description', 'template_config', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True, allow_null=True)
    generated_by_username = serializers.CharField(source='generated_by.username', read_only=True, allow_null=True)
    school_name = serializers.CharField(source='school.name', read_only=True, allow_null=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True, allow_null=True)
    student_username = serializers.CharField(source='student.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'template', 'template_name', 'report_type', 'title',
            'generated_by', 'generated_by_username', 'school', 'school_name',
            'class_obj', 'class_name', 'student', 'student_username',
            'filters', 'data', 'generated_at', 'file_path', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'generated_at', 'created_at', 'updated_at']

