from .models import Project
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'github_url', 'live_url', 'technologies', 'project_image', 'owner']
        read_only_fields = ['id', 'owner']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Description cannot be empty.")
        return value

    def validate_github_url(self, value):
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("GitHub URL must be a valid URL.")
        return value