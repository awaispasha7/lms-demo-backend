from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolicyViewSet, PolicyViolationViewSet, BehaviorIncidentViewSet

router = DefaultRouter()
router.register(r'policies', PolicyViewSet, basename='policies')
router.register(r'violations', PolicyViolationViewSet, basename='violations')
router.register(r'incidents', BehaviorIncidentViewSet, basename='incidents')

urlpatterns = [
    path('', include(router.urls)),
]

