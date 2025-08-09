from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializer import CustomUserSerializer, RegisterUserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login

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
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')
        else:
            return render(request, 'registration/register.html', {'form': serializer.errors})
    else:
        serializer = RegisterUserSerializer()
    return render(request, 'registration/register.html', {'form': serializer})


