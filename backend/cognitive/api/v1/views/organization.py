import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, utils
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers, status

from cognitive.api.v1.permissions import (
    AdminPermissions,
    ClientPermissions,
    HasOrganizationAPIKey,
    ManagerPermissions
)
from cognitive.api.v1.serializers.organization import (
    OrganizationCreateUpdateSerializer,
    OrganizationListSerializer,
    SignMessageSerializer
)
from cognitive.api.v1.viewsets import ExtendedModelViewSet
from cognitive.apps.organization.models import Organization, OrganizationAPIKey
from cognitive.apps.transaction.models import Transaction


def parse_organization_key(key):
    key = key[:31] + '\n' + key[31:]
    key = key[:-29] + '\n' + key[-29:]
    key = serialization.load_pem_private_key(str.encode(key), password=None)
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
        'sign_message': SignMessageSerializer
    }

    permission_map = {
        'list': (AdminPermissions | ManagerPermissions | ClientPermissions),
        'create': AdminPermissions,
        'destroy': AdminPermissions,
        'update': AdminPermissions,
        'partial_update': AdminPermissions,
        'get_new_key': (AdminPermissions | ManagerPermissions | ClientPermissions),
        'sign_message': HasOrganizationAPIKey
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if AdminPermissions().has_permission(self.request, self):
            return queryset
        if ManagerPermissions().has_permission(self.request, self) and self.action == 'list':
            queryset = queryset.filter(
                organization__users__exact=self.request.user.pk)
        if ClientPermissions().has_permission(self.request, self) and self.action == 'list':
            queryset = queryset.filter(
                organization__users__exact=self.request.user.pk)

        return queryset

    @action(methods=['get'], detail=True, url_path='generate_key')
    def get_new_key(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)

        api_key, key = OrganizationAPIKey.objects.create_key(
            organization=organization, name=f'{organization.name}_api_key')

        return Response(key)

    @action(methods=['post'], detail=False, url_path='sign_message')
    def sign_message(self, request):

        try:
            key = request.META["HTTP_X_API_KEY"]
        except Exception:
            return serializers.ValidationError()
        try:
            organization = OrganizationAPIKey.objects.get_from_key(
                key).organization
        except Exception:
            return serializers.ValidationError()

        # serialize and validate payload
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # check organization balance and status
        if organization.status == Organization.Status.BLOCKED:
            error = {'errors': {'balance': 'organization is blocked'}}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if not organization.balance:
            error = {'errors': {'balance': 'low balance'}}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        # prepare organization RSA key
        sign_key = organization.hashed_key
        sign_key = sign_key[:31] + '\n' + sign_key[31:]
        sign_key = sign_key[:-29] + '\n' + sign_key[-29:]
        sign_key = serialization.load_pem_private_key(str.encode(sign_key), password=None)

        # sign message
        try:
            message_bytes = base64.b64decode(serializer['message'].value)
            signature = sign_key.sign(message_bytes, padding.PKCS1v15(), utils.Prehashed(hashes.SHA1()))
            signed_message = base64.b64encode(signature).decode()
        except ValueError as e:
            error = {'errors': {'error': f'{e}'}}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        # create transaction and update organization balance
        Transaction.objects.create(organization=organization)
        organization.balance -= 1
        organization.save()

        # prepare response data
        response_data = {'message': signed_message}

        return Response(response_data, status=status.HTTP_200_OK)
