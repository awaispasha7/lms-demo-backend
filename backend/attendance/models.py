from django.db import models
from django.conf import settings


class Attendance(models.Model):
    """Attendance model"""
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('EXCUSED', 'Excused'),
        ('PARTIAL', 'Partial'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    class_obj = models.ForeignKey('academics.Class', on_delete=models.CASCADE, related_name='attendances', db_column='class_obj_id')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENT')
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_attendances')
    marked_at = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'attendance'
        unique_together = ['student', 'class_obj', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.username} - {self.class_obj.name} - {self.date} - {self.status}"


class AttendanceReport(models.Model):
    """Attendance Report model"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_reports')
    class_obj = models.ForeignKey('academics.Class', on_delete=models.CASCADE, related_name='attendance_reports', db_column='class_obj_id')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField(default=0)
    present_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    late_days = models.IntegerField(default=0)
    excused_days = models.IntegerField(default=0)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'attendance_reports'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"Attendance Report - {self.student.username} - {self.start_date} to {self.end_date}"

