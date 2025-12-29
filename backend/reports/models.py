from django.db import models
from django.db.models import JSONField
from django.conf import settings


class ReportTemplate(models.Model):
    """Report Template model"""
    REPORT_TYPE_CHOICES = [
        ('PERFORMANCE', 'Performance'),
        ('ATTENDANCE', 'Attendance'),
        ('BEHAVIOR', 'Behavior'),
        ('ASSIGNMENT', 'Assignment'),
        ('COMPREHENSIVE', 'Comprehensive'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    template_config = JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'report_templates'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.report_type})"


class Report(models.Model):
    """Report model"""
    REPORT_TYPE_CHOICES = [
        ('PERFORMANCE', 'Performance'),
        ('ATTENDANCE', 'Attendance'),
        ('BEHAVIOR', 'Behavior'),
        ('ASSIGNMENT', 'Assignment'),
        ('COMPREHENSIVE', 'Comprehensive'),
    ]
    
    template = models.ForeignKey(ReportTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_reports')
    school = models.ForeignKey('academics.School', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    class_obj = models.ForeignKey('academics.Class', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports', db_column='class_obj_id')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_reports')
    filters = JSONField(default=dict, blank=True)
    data = JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} - {self.report_type}"

