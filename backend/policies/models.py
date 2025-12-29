from django.db import models
from django.conf import settings


class Policy(models.Model):
    """Policy model"""
    school = models.ForeignKey('academics.School', on_delete=models.SET_NULL, null=True, blank=True, related_name='policies')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'policies'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class PolicyViolation(models.Model):
    """Policy Violation model"""
    VIOLATION_TYPE_CHOICES = [
        ('ACADEMIC_INTEGRITY', 'Academic Integrity'),
        ('BEHAVIOR', 'Behavior'),
        ('ATTENDANCE', 'Attendance'),
        ('DRESS_CODE', 'Dress Code'),
        ('OTHER', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    school = models.ForeignKey('academics.School', on_delete=models.SET_NULL, null=True, blank=True, related_name='violations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='violations')
    policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True, related_name='violations')
    violation_type = models.CharField(max_length=20, choices=VIOLATION_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MEDIUM')
    description = models.TextField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_violations')
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True, null=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_violations')
    resolved_at = models.DateTimeField(null=True, blank=True)
    ai_flagged = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'policy_violations'
        ordering = ['-reported_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.violation_type}"


class BehaviorIncident(models.Model):
    """Behavior Incident model"""
    INCIDENT_TYPE_CHOICES = [
        ('DISRUPTIVE', 'Disruptive'),
        ('BULLYING', 'Bullying'),
        ('VIOLENCE', 'Violence'),
        ('THEFT', 'Theft'),
        ('VANDALISM', 'Vandalism'),
        ('SUBSTANCE_ABUSE', 'Substance Abuse'),
        ('OTHER', 'Other'),
    ]
    
    school = models.ForeignKey('academics.School', on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incidents')
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True)
    incident_date = models.DateTimeField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_incidents')
    reported_at = models.DateTimeField(auto_now_add=True)
    witnesses = models.TextField(blank=True, null=True)
    action_taken = models.TextField(blank=True, null=True)
    resolved = models.BooleanField(default=False)
    ai_flagged = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'behavior_incidents'
        ordering = ['-incident_date']
    
    def __str__(self):
        return f"{self.student.username} - {self.incident_type} - {self.incident_date}"

