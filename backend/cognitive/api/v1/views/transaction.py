from cognitive.api.v1.permissions import ClientPermissions
from cognitive.api.v1.permissions import AdminPermissions, ManagerPermissions
from cognitive.api.v1.serializers.transaction import TransactionFullSerializer
from cognitive.api.v1.viewsets import ExtendedModelViewSet
from cognitive.apps.transaction.models import Transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class TransactionViewSet(ExtendedModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionFullSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]

    filterset_fields = ('organization__name', 'organization')
    ordering_fields = ('id')
    search_fields = ('organization__name')

    permission_map = {
        'list': permissions.IsAuthenticated,
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
