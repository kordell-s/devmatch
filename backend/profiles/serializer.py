from .models import Developer
from rest_framework import serializers
from accounts.models import CustomUser


class CustomUserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']
        read_only_fields = fields


class DeveloperSerializer(serializers.ModelSerializer):
    user = CustomUserNestedSerializer(read_only=True)

    class Meta:
        model = Developer
        fields = [
            'id', 'user', 'bio', 'location', 'skills', 'resume',
            'video_intro', 'github_url', 'experience', 'portfolio_url'
        ]
        read_only_fields = ['id', 'user']
