from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register_view, custom_logout_view
from django.contrib.auth.views import LoginView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_view, name='register'),
    path('register/user/', register_view, name='register-user'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),  # 
]


