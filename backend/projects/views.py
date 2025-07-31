from rest_framework import viewsets, permissions
from .models import Project
from profiles.models import Developer
from .serializer import ProjectSerializer

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically associate the project with the authenticated user
        if not self.request.user.is_authenticated:
            raise permissions.PermissionDenied("You must be logged in to create a project.")
        serializer.save(owner=self.request.user)
