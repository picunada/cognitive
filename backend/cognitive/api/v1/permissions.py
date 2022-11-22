from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from rest_framework_api_key.permissions import BaseHasAPIKey

from cognitive.apps.organization.models import OrganizationAPIKey
from cognitive.apps.user.models import Roles

User = get_user_model()


class AdminPermissions(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.role == Roles.ADMINISTRATOR)
        )


class ManagerPermissions(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == Roles.MANAGER)


class ClientPermissions(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == Roles.CLIENT)


class HasOrganizationAPIKey(BaseHasAPIKey):
    model = OrganizationAPIKey
