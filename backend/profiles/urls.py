from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeveloperViewSet, developer_list, developer_detail

# API router
router = DefaultRouter()
router.register(r'developers', DeveloperViewSet, basename='developer')

# Template URLs (no 'api/' prefix)
urlpatterns = [
    path('list/', developer_list, name='developers-list'),
    path('<int:pk>/', developer_detail, name='devDetails'),
]

# API URLs will be included separately
api_urlpatterns = [
    path('', include(router.urls)),
]