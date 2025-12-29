from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Policy, PolicyViolation, BehaviorIncident
from .serializers import PolicySerializer, PolicyViolationSerializer, BehaviorIncidentSerializer


class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class PolicyViolationViewSet(viewsets.ModelViewSet):
    queryset = PolicyViolation.objects.all()
    serializer_class = PolicyViolationSerializer
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve a violation"""
        violation = self.get_object()
        resolution_notes = request.data.get('resolution_notes', '')
        
        violation.resolved = True
        violation.resolution_notes = resolution_notes
        violation.resolved_by = request.user if request.user.is_authenticated else None
        violation.resolved_at = timezone.now()
        violation.save()
        
        serializer = self.get_serializer(violation)
        return Response(serializer.data)


class BehaviorIncidentViewSet(viewsets.ModelViewSet):
    queryset = BehaviorIncident.objects.all()
    serializer_class = BehaviorIncidentSerializer
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an incident"""
        incident = self.get_object()
        action_taken = request.data.get('action_taken', '')
        
        incident.resolved = True
        incident.action_taken = action_taken
        incident.save()
        
        serializer = self.get_serializer(incident)
        return Response(serializer.data)

