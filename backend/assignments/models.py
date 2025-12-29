from django.db import models
from django.db.models import JSONField
from django.conf import settings


class Assignment(models.Model):
    """
    Assignment model matching the API structure.
    Questions are stored as JSONB in the questions field.
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('CLOSED', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_assignments')
    class_obj = models.ForeignKey('academics.Class', on_delete=models.CASCADE, related_name='assignments', db_column='class_obj_id')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    instructions = models.TextField(blank=True, null=True)
    questions = JSONField(
        default=list,
        help_text="Array of question objects with questionNumber, questionText, options, correctOptions, rubric, marks, type"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assignments'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_total_marks(self):
        """Calculate total marks from questions"""
        if not self.questions:
            return 0
        return sum(q.get('marks', 0) for q in self.questions if isinstance(q, dict))


class Submission(models.Model):
    """
    Submission model matching the API structure.
    Supports both student FK (for API) and student_name (for backward compatibility).
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('LATE', 'Late'),
        ('GRADED', 'Graded'),
    ]
    
    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE, 
        related_name='submissions',
        db_column='assignment_id'
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    student_name = models.TextField(blank=True, null=True)  # For backward compatibility
    submission_text = models.TextField(blank=True, null=True)
    answers = JSONField(
        default=list,
        help_text="Array of answer objects with questionNumber, selectedOptions, textAnswer, etc."
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    is_active = models.BooleanField(default=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'submissions'
        ordering = ['-submitted_at']
    
    def __str__(self):
        student_identifier = self.student.username if self.student else self.student_name
        return f"{student_identifier} - {self.assignment.title}"


class Grade(models.Model):
    """Grade model matching the API structure"""
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    score = models.DecimalField(max_digits=10, decimal_places=2)
    max_score = models.DecimalField(max_digits=10, decimal_places=2)
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')
    graded_at = models.DateTimeField(auto_now_add=True)
    ai_suggested_score = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ai_suggested_feedback = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grades'
        ordering = ['-graded_at']
    
    @property
    def percentage(self):
        if self.max_score and self.max_score > 0:
            return (self.score / self.max_score) * 100
        return 0
    
    def __str__(self):
        return f"{self.submission} - {self.score}/{self.max_score}"

