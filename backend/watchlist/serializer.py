from .models import Watchlist
from rest_framework import serializers
from profiles.serializer import DeveloperSerializer
from django.core.exceptions import ValidationError as DjangoValidationError


class WatchlistSerializer(serializers.ModelSerializer):
    developer_details = DeveloperSerializer(source='developer', read_only=True)
    recruiter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Watchlist
        fields = ['id', 'recruiter', 'developer', 'saved_at', 'developer_details']
        read_only_fields = ['saved_at']

    def validate_recruiter(self, value):
        if value.user_type != 'recruiter':
            raise serializers.ValidationError("Only recruiters can create watchlist entries.")
        return value

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                raise serializers.ValidationError(e.message_dict)
            else:
                raise serializers.ValidationError(str(e))