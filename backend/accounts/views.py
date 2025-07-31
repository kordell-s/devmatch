from rest_framework import generics
from .models import CustomUser
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer

# Create your views here.

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'developer')
        )
        return user
    
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


