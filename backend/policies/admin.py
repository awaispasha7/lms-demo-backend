from django.contrib import admin
from .models import Policy, PolicyViolation, BehaviorIncident


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'school', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']


@admin.register(PolicyViolation)
class PolicyViolationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'violation_type', 'severity', 'resolved', 'reported_at']
    list_filter = ['violation_type', 'severity', 'resolved']
    search_fields = ['user__username', 'description']


@admin.register(BehaviorIncident)
class BehaviorIncidentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'incident_type', 'incident_date', 'resolved', 'reported_at']
    list_filter = ['incident_type', 'resolved']
    search_fields = ['student__username', 'description']

