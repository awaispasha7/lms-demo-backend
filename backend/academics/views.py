from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import AcademicYear, Subject, Class, School, StudentClass, TeacherSubjectClass
from .serializers import (
    AcademicYearSerializer, SubjectSerializer, ClassSerializer,
    SchoolSerializer, StudentClassSerializer, TeacherSubjectClassSerializer
)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current academic year"""
        year = AcademicYear.objects.filter(is_current=True).first()
        if year:
            serializer = self.get_serializer(year)
            return Response(serializer.data)
        return Response({'error': 'No current academic year set'}, status=status.HTTP_404_NOT_FOUND)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class StudentClassViewSet(viewsets.ModelViewSet):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer


class TeacherSubjectClassViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubjectClass.objects.all()
    serializer_class = TeacherSubjectClassSerializer
