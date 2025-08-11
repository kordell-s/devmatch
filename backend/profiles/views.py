from rest_framework import viewsets, permissions
from .models import Developer
from .forms import DeveloperForm
from .serializer import DeveloperSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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


@login_required
def edit_developer_profile(request):
    developer_profile, crreated = Developer.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = DeveloperForm(request.POST, request.FILES, instance=developer_profile)
        if form.is_valid():
            form.save()
            return redirect('devDetails', pk=developer_profile.pk)
    else:
        form = DeveloperForm(instance=developer_profile)
    return render(request, 'developers/editProfile.html', {'form': form})