from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, register, login, profile, change_password

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('', include(router.urls)),
]
