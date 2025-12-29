from django.db import models
from django.conf import settings


class School(models.Model):
    """School model"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'schools'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    """Academic Year model"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'academic_years'
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name


class Subject(models.Model):
    """Subject model"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    credit_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subjects'
        unique_together = ['school', 'code']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Class(models.Model):
    """Class model"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    grade_level = models.IntegerField()
    capacity = models.IntegerField(null=True, blank=True)
    class_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='taught_classes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'classes'
        unique_together = ['school', 'code']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"


class StudentClass(models.Model):
    """Student-Class Enrollment model"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments', db_column='class_obj_id')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_enrollments'
        unique_together = ['student', 'class_obj', 'academic_year']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.student.username} - {self.class_obj.name}"


class TeacherSubjectClass(models.Model):
    """Teacher-Subject-Class Assignment model"""
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_assignments')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='teacher_assignments', db_column='class_obj_id')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='teacher_assignments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teacher_subject_classes'
        unique_together = ['teacher', 'subject', 'class_obj', 'academic_year']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.teacher.username} - {self.subject.name} - {self.class_obj.name}"

