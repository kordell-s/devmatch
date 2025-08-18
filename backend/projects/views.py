from rest_framework import viewsets, permissions
from .models import Project
from profiles.models import Developer
from .serializer import ProjectSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProjectForm
from django.http import JsonResponse

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

@login_required
def add_project(request):
    """Add a new project for the authenticated user"""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Project added successfully!')
            
            # Redirect to developer profile if exists, otherwise to projects list
            if hasattr(request.user, 'developer_profile'):
                return redirect('developer-detail', pk=request.user.developer_profile.pk)
            return redirect('developers-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/add_project.html', {'form': form})

@login_required
def edit_project(request, pk):
    """Edit an existing project (only by the owner)"""
    project = get_object_or_404(Project, pk=pk)
    
    # Check if user is the owner
    if project.owner != request.user:
        messages.error(request, "You can only edit your own projects.")
        return redirect('developer-detail', pk=request.user.developer_profile.pk if hasattr(request.user, 'developer_profile') else 'developers-list')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            
            if hasattr(request.user, 'developer_profile'):
                return redirect('developer-detail', pk=request.user.developer_profile.pk)
            return redirect('developers-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    """Delete a project (only by the owner)"""
    project = get_object_or_404(Project, pk=pk)
    
    # Check if user is the owner
    if project.owner != request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'You can only delete your own projects.'})
        messages.error(request, "You can only delete your own projects.")
        return redirect('developer-detail', pk=request.user.developer_profile.pk if hasattr(request.user, 'developer_profile') else 'developers-list')
    
    if request.method == 'POST':
        project_title = project.title
        project.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'"{project_title}" has been deleted successfully.'})
        
        messages.success(request, f'Project "{project_title}" has been deleted successfully!')
        if hasattr(request.user, 'developer_profile'):
            return redirect('developer-detail', pk=request.user.developer_profile.pk)
        return redirect('developers-list')
    
    # For non-AJAX requests, redirect back
    messages.error(request, "Invalid request method.")
    if hasattr(request.user, 'developer_profile'):
        return redirect('developer-detail', pk=request.user.developer_profile.pk)
    return redirect('developers-list')
