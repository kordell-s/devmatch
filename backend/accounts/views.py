from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializer import CustomUserSerializer, RegisterUserSerializer

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


