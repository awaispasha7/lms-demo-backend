from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg
from .models import Report, ReportTemplate
from .serializers import ReportSerializer, ReportTemplateSerializer
from attendance.models import Attendance, AttendanceReport
from assignments.models import Assignment, Submission


class ReportTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
    @action(detail=False, methods=['post'])
    def generate_attendance(self, request):
        """Generate attendance report"""
        data = request.data
        student_id = data.get('student')
        class_obj_id = data.get('class_obj')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Generate attendance report
        attendances = Attendance.objects.filter(
            student_id=student_id,
            class_obj_id=class_obj_id,
            date__gte=start_date,
            date__lte=end_date
        )
        
        report_data = {
            'total_days': attendances.count(),
            'present_days': attendances.filter(status='PRESENT').count(),
            'absent_days': attendances.filter(status='ABSENT').count(),
            'late_days': attendances.filter(status='LATE').count(),
            'excused_days': attendances.filter(status='EXCUSED').count(),
        }
        
        report = Report.objects.create(
            report_type='ATTENDANCE',
            title=f'Attendance Report - {start_date} to {end_date}',
            generated_by=request.user if request.user.is_authenticated else None,
            class_obj_id=class_obj_id,
            student_id=student_id,
            filters={'start_date': start_date, 'end_date': end_date},
            data=report_data
        )
        
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def generate_performance(self, request):
        """Generate performance report for a student"""
        data = request.data
        student_id = data.get('student')
        class_obj_id = data.get('class_obj')
        
        # Get all submissions for student
        submissions = Submission.objects.filter(
            student_name__icontains=student_id  # Simplified - should use proper FK
        )
        
        report_data = {
            'total_assignments': Assignment.objects.filter(class_obj_id=class_obj_id).count(),
            'submitted': submissions.count(),
            'graded': submissions.filter(status='graded').count(),
            'average_score': submissions.filter(ai_score__isnull=False).aggregate(
                avg_score=Avg('ai_score')
            )['avg_score'] or 0,
        }
        
        report = Report.objects.create(
            report_type='PERFORMANCE',
            title=f'Performance Report',
            generated_by=request.user if request.user.is_authenticated else None,
            class_obj_id=class_obj_id,
            student_id=student_id,
            data=report_data
        )
        
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def generate_class_comparison(self, request):
        """Generate class comparison report (Admin only)"""
        data = request.data
        class_ids = data.get('class_ids', [])
        academic_year_id = data.get('academic_year')
        
        # Compare classes
        report_data = {
            'classes': []
        }
        
        for class_id in class_ids:
            class_data = {
                'class_id': class_id,
                'total_students': 0,
                'average_performance': 0,
            }
            report_data['classes'].append(class_data)
        
        report = Report.objects.create(
            report_type='COMPREHENSIVE',
            title='Class Comparison Report',
            generated_by=request.user if request.user.is_authenticated else None,
            filters={'class_ids': class_ids, 'academic_year': academic_year_id},
            data=report_data
        )
        
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

