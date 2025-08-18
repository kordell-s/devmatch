from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializer import CustomUserSerializer, RegisterUserSerializer
from .forms import DeveloperRegistrationForm, RecruiterRegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from profiles.models import Developer, Recruiter

# Create your views here.

class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer  # This serializer handles user registration
    permission_classes = [permissions.AllowAny] 


class CurrentUserViewSet(viewsets.ModelViewSet):     
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user     # This will return the currently authenticated user
    

def register_view(request):
    """Main registration page that shows role selection"""
    return render(request, 'registration/register.html')

def register_developer_view(request):
    if request.method == 'POST':
        form = DeveloperRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create developer profile instance
            developer_profile = Developer.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Please complete your developer profile.")
            return redirect('edit-developer-profile')  # Redirect to profile completion
        else:
            return render(request, 'registration/register_developer.html', {'form': form})
    else:
        form = DeveloperRegistrationForm()
    return render(request, 'registration/register_developer.html', {'form': form})


def register_recruiter_view(request):
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create recruiter profile instance
            recruiter_profile = Recruiter.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your recruiter account has been created.")
            return redirect('developers-list')  # Recruiters can browse immediately
        else:
            return render(request, 'registration/register_recruiter.html', {'form': form})
    else:
        form = RecruiterRegistrationForm()
    return render(request, 'registration/register_recruiter.html', {'form': form})


def home(request):
    return redirect('developers-list')


def custom_logout_view(request):
    if request.user.is_authenticated:
        user_name = request.user.username or request.user.get_full_name()
        logout(request)
        messages.success(request, f"You have successfully logged out, {user_name}.")
    else:
        messages.info(request, "You are already logged out.")
    
    return redirect('developers-list')

