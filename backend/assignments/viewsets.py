from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Assignment, Submission, Grade
from .serializers import (
    AssignmentSerializer, SubmissionSerializer, GradeSerializer,
    AssignmentCreateSerializer, SubmissionCreateSerializer, GradeCreateSerializer
)
from .services import auto_grade_submission, generate_encouraging_feedback


class AssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Assignment management matching API structure"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AssignmentCreateSerializer
        return AssignmentSerializer
    
    @action(detail=True, methods=['post'])
    def ai_grade(self, request, pk=None):
        """AI grading suggestion for assignment"""
        assignment = self.get_object()
        # Placeholder - integrate with AI service
        return Response({
            'message': 'AI grading suggestion endpoint',
            'assignment_id': assignment.id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get all submissions for an assignment"""
        assignment = self.get_object()
        submissions = assignment.submissions.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Student submits assignment"""
        assignment = self.get_object()
        serializer = SubmissionCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            submission = serializer.save(
                assignment=assignment,
                student=request.user if request.user.is_authenticated else None,
                status='SUBMITTED',
                submitted_at=timezone.now()
            )
            return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for Submission management matching API structure"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SubmissionCreateSerializer
        return SubmissionSerializer


class GradeViewSet(viewsets.ModelViewSet):
    """ViewSet for Grade management matching API structure"""
    queryset = Grade.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return GradeCreateSerializer
        return GradeSerializer

