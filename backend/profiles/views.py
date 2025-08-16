from rest_framework import viewsets, permissions
from .models import Developer
from django.db.models import Q
from .forms import DeveloperForm
from .serializer import DeveloperSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.filter(user__role='developer')
    serializer_class = DeveloperSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def developer_list(request):
    developers = Developer.objects.all()
    
    # Get all unique skills for the filter
    all_skills = set()
    for dev in Developer.objects.all():
        if dev.skills:
            all_skills.update(dev.skills)
    all_skills = sorted(list(all_skills))
    
    # Search functionality for non-AJAX requests
    search_query = request.GET.get('search')
    if search_query:
        developers = developers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(skills__icontains=search_query)
        ).distinct()
    
    # Skill filter functionality
    skill_filter = request.GET.get('skill')
    if skill_filter:
        developers = developers.filter(skills__contains=[skill_filter])
    
    return render(request, 'developers/devList.html', {
        'developers': developers,
        'all_skills': all_skills,
    })

def developer_detail(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    return render(request, 'developers/devDetails.html', {'developer': developer})

@login_required
def edit_developer_profile(request):
    developer_profile, created = Developer.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = DeveloperForm(request.POST, request.FILES, instance=developer_profile)
        if form.is_valid():
            developer = form.save(commit=False)
            developer.user = request.user  # Ensure the user is set
            developer.save()
            if developer.profile_picture:
                print(f"Profile picture URL: {developer.profile_picture.url}")
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('developer-detail', pk=developer.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DeveloperForm(instance=developer_profile)
    
    return render(request, 'developers/editProfile.html', {'form': form})

def developer_search_ajax(request):
    """AJAX endpoint for developer search"""
    developers = Developer.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        developers = developers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(skills__icontains=search_query)
        ).distinct()

    # Skill filter functionality - FIXED: Added double underscore
    skill_filter = request.GET.get('skill')
    if skill_filter:
        developers = developers.filter(skills__contains=[skill_filter])

    # Serialize data with proper error handling
    developers_data = []
    for dev in developers:
        try:
            developers_data.append({
                'id': dev.id,
                'username': dev.user.username,
                'first_name': dev.user.first_name or '',
                'last_name': dev.user.last_name or '',
                'profile_picture': dev.profile_picture.url if dev.profile_picture else None,
                'bio': dev.bio or '',
                'skills': dev.skills or [],
                'github_url': dev.github_url or '',
                'portfolio_url': dev.portfolio_url or ''
            })
        except Exception as e:
            # Log the error but continue processing other developers
            print(f"Error processing developer {dev.id}: {e}")
            continue
    
    # Return proper JSON response format expected by JavaScript
    return JsonResponse({'developers': developers_data})