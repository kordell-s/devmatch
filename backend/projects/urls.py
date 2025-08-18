from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, add_project, edit_project, delete_project

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    # Template-based URLs
    path('add/', add_project, name='add-project'),
    path('<int:pk>/edit/', edit_project, name='edit-project'),
    path('<int:pk>/delete/', delete_project, name='delete-project'),
    
    # API URLs
    path('', include(router.urls)),
]