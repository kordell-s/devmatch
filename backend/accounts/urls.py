from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, CurrentUserViewSet

router = DefaultRouter()
router.register(r'register', RegisterUserViewSet, basename='register')
router.register(r'current', CurrentUserViewSet, basename='current-user')

urlpatterns = [
    path('', include(router.urls)),
]


