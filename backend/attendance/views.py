from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from .models import Attendance, AttendanceReport
from .serializers import AttendanceSerializer, AttendanceReportSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    @action(detail=False, methods=['post'])
    def mark_bulk(self, request):
        """Mark attendance for multiple students at once"""
        data = request.data
        class_obj_id = data.get('class_obj')
        date = data.get('date')
        attendances = data.get('attendances', [])
        
        created_count = 0
        for att_data in attendances:
            serializer = AttendanceSerializer(data={
                'student': att_data.get('student'),
                'class_obj': class_obj_id,
                'date': date,
                'status': att_data.get('status', 'PRESENT'),
                'remarks': att_data.get('remarks', ''),
                'marked_by': request.user.id if request.user.is_authenticated else None,
            })
            if serializer.is_valid():
                serializer.save()
                created_count += 1
        
        return Response({
            'message': f'Marked attendance for {created_count} students',
            'count': created_count
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get attendance statistics"""
        class_obj_id = request.query_params.get('class_obj')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = Attendance.objects.all()
        
        if class_obj_id:
            queryset = queryset.filter(class_obj_id=class_obj_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        stats = queryset.values('status').annotate(count=Count('id'))
        
        return Response({
            'statistics': list(stats),
            'total': queryset.count()
        })


class AttendanceReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate attendance report for a student"""
        data = request.data
        student_id = data.get('student')
        class_obj_id = data.get('class_obj')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Calculate attendance statistics
        attendances = Attendance.objects.filter(
            student_id=student_id,
            class_obj_id=class_obj_id,
            date__gte=start_date,
            date__lte=end_date
        )
        
        total_days = attendances.count()
        present_days = attendances.filter(status='PRESENT').count()
        absent_days = attendances.filter(status='ABSENT').count()
        late_days = attendances.filter(status='LATE').count()
        excused_days = attendances.filter(status='EXCUSED').count()
        
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        report = AttendanceReport.objects.create(
            student_id=student_id,
            class_obj_id=class_obj_id,
            start_date=start_date,
            end_date=end_date,
            total_days=total_days,
            present_days=present_days,
            absent_days=absent_days,
            late_days=late_days,
            excused_days=excused_days,
            attendance_percentage=attendance_percentage
        )
        
        serializer = AttendanceReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

