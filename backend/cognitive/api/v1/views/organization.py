import base64

from cognitive.api.v1.permissions import (AdminPermissions,
                                          HasOrganizationAPIKey,
                                          ManagerPermissions)
from cognitive.api.v1.serializers.organization import (
    OrganizationCreateUpdateSerializer, OrganizationListSerializer,
    SignMessageSerializer)
from cognitive.api.v1.viewsets import ExtendedModelViewSet
from cognitive.apps.organization.models import Organization, OrganizationAPIKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, utils
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import serializers


def get_key(key):
    open("key", "w").write(key)
    with open('key', 'rb') as keyfile:
        key = serialization.load_pem_private_key(keyfile.read(), password=None)
    return key


class OrganizationViewSet(ExtendedModelViewSet):
    queryset = Organization.objects.non_deleted()
    serializer_class = OrganizationListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ('name', 'created_at')
    search_fields = ('name',)
    ordering_fields = ('created_at', )

    serializer_class_map = {
        'list': OrganizationListSerializer,
        'create': OrganizationCreateUpdateSerializer,
        'update': OrganizationCreateUpdateSerializer,
        'partial_update': OrganizationCreateUpdateSerializer,
        'block': OrganizationCreateUpdateSerializer,
        'unblock': OrganizationCreateUpdateSerializer,
        'sign_message': SignMessageSerializer
    }

    permission_map = {
        'list': permissions.AllowAny,
        'create': permissions.AllowAny,
        'destroy': permissions.AllowAny,
        'update': permissions.AllowAny,
        'partial_update': permissions.AllowAny,
        'get_new_key': permissions.AllowAny,
        'block': permissions.AllowAny,
        'unblock': permissions.AllowAny,
        'sign_message': HasOrganizationAPIKey
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    @action(methods=['get'], detail=True, url_path='generate_key')
    def get_new_key(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)

        api_key, key = OrganizationAPIKey.objects.create_key(
            organization=organization, name=f'{organization.name}_api_key')

        return Response(key)

    @action(methods=['get'], detail=True, url_path='block')
    def block(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        organization.status = "blocked"
        organization.save()

        serializer = self.get_serializer(instance=organization)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='unblock')
    def unblock(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        organization.status = "active"
        organization.save()

        serializer = self.get_serializer(instance=organization)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='sign_message')
    def sign_message(self, request):

        try:
            key = request.META["HTTP_X_API_KEY"]
        except Exception:
            return serializers.ValidationError()
        try:
            api_key = OrganizationAPIKey.objects.get_from_key(key)
            organization = Organization.objects.get(api_keys=api_key)
        except Exception:
            return serializers.ValidationError()

        print(organization.hashed_key)

        sign_key = get_key(organization.hashed_key)

        print(request.data['message'])

        message_bytes = base64.b64decode(request.data['message'])
        signature = sign_key.sign(
            message_bytes, padding.PKCS1v15(), utils.Prehashed(hashes.SHA1()))
        signed_message = base64.b64encode(signature).decode()

        return Response({'status': 'ok', 'message': signed_message})
