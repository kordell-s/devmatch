from rest_framework import viewsets, permissions
from .models import Developer
from .serializer import DeveloperSerializer


# Create your views here.

class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.filter(user__role='developer')
    serializer_class = DeveloperSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically associate the developer profile with the authenticated user