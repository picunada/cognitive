from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from cognitive.apps.organization.models import Organization, OrganizationAPIKey

User = get_user_model()


class OrganizationFullSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'hashed_key',
                  'status', 'created_at', 'deleted_at')
        read_only_fields = ('id', 'created_at')
        model = Organization


class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Serializer for list Organization model.
    """

    class Meta:
        fields = ('id', 'name', 'hashed_key', 'api_keys',
                  'status', 'created_at', 'deleted_at')
        read_only_fields = ('id', 'created_at')
        model = Organization


class OrganizationCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for create and update Organization model.
    """

    class Meta:
        fields = ('id', 'name', 'hashed_key',
                  'status', 'created_at', 'deleted_at')
        read_only_fields = ('id', 'created_at', 'deleted_at')
        model = Organization

    def create(self, data):
        organization = super().create(data)

        organization.save()

        return organization


class SignMessageSerializer(serializers.Serializer):

    message = serializers.CharField()
