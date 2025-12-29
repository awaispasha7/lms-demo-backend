from rest_framework import serializers
from .models import Policy, PolicyViolation, BehaviorIncident


class PolicySerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Policy
        fields = [
            'id', 'school', 'school_name', 'title', 'description',
            'category', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PolicyViolationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)
    policy_title = serializers.CharField(source='policy.title', read_only=True, allow_null=True)
    school_name = serializers.CharField(source='school.name', read_only=True, allow_null=True)
    reported_by_username = serializers.CharField(source='reported_by.username', read_only=True, allow_null=True)
    resolved_by_username = serializers.CharField(source='resolved_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = PolicyViolation
        fields = [
            'id', 'school', 'school_name', 'user', 'user_username', 'user_email', 'user_role',
            'policy', 'policy_title', 'violation_type', 'severity', 'description',
            'reported_by', 'reported_by_username', 'reported_at', 'resolved',
            'resolution_notes', 'resolved_by', 'resolved_by_username', 'resolved_at',
            'ai_flagged', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'reported_at', 'resolved_at', 'created_at', 'updated_at'
        ]


class BehaviorIncidentSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True, allow_null=True)
    reported_by_username = serializers.CharField(source='reported_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = BehaviorIncident
        fields = [
            'id', 'school', 'school_name', 'student', 'student_username', 'student_email',
            'incident_type', 'description', 'location', 'incident_date',
            'reported_by', 'reported_by_username', 'reported_at', 'witnesses',
            'action_taken', 'resolved', 'ai_flagged', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reported_at', 'created_at', 'updated_at']

