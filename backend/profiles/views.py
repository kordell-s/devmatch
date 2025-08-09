from rest_framework import viewsets, permissions
from .models import Developer
from .serializer import DeveloperSerializer
from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.

class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.filter(user__role='developer')
    serializer_class = DeveloperSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically associate the developer profile with the authenticated user

def developer_list(request):
    developers = Developer.objects.all()
    return render(request, 'developers/devList.html', {'developers': developers})

def developer_detail(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    return render(request, 'developers/devDetails.html', {'developer': developer})