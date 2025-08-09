from .models import Developer, Recruiter
from rest_framework import serializers
from accounts.models import CustomUser


class CustomUserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'profile_photo', 'email', 'role', 'first_name', 'last_name']
        read_only_fields = fields


class DeveloperSerializer(serializers.ModelSerializer):
    user = CustomUserNestedSerializer(read_only=True)

    class Meta:
        model = Developer
        fields = [
            'id', 'user', 'profile_picture','bio', 'location', 'skills', 'resume',
            'video_intro', 'github_url', 'experience', 'portfolio_url'
        ]
        read_only_fields = ['id', 'user']


class RecruiterSerializer(serializers.ModelSerializer):
    user = CustomUserNestedSerializer(read_only=True)

    class Meta:
        model = Recruiter
        fields = [
            'id', 'user', 'company_name', 'company_website', 'company_description'
        ]
        read_only_fields = ['id', 'user']
