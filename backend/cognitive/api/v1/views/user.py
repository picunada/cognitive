from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from cognitive.api.v1.permissions import AdminPermissions
from cognitive.api.v1.serializers.user import UserCreateUpdateSerializer, UserFullSerializer, \
    PasswordResetSerializer, PasswordResetConfirmSerializer
from cognitive.api.v1.viewsets import ExtendedModelViewSet

User = get_user_model()


class UserViewSet(ExtendedModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserFullSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]

    filterset_fields = ('role', 'organization__name', 'organization')
    ordering_fields = ('date_joined', 'id')
    search_fields = ('first_name', 'last_name')

    serializer_class_map = {
        'create': UserCreateUpdateSerializer,
        'update': UserCreateUpdateSerializer,
        'partial_update': UserCreateUpdateSerializer,
        # 'password_reset': PasswordResetSerializer,
        # 'password_reset_confirm': PasswordResetConfirmSerializer
    }

    permission_map = {
        'create': permissions.AllowAny,
        'list': permissions.AllowAny,
        'update': (AdminPermissions | permissions.IsAuthenticated),
        'partial_update': (AdminPermissions | permissions.IsAuthenticated),
        'delete': AdminPermissions,
        'my': permissions.IsAuthenticated,
        # 'password_reset': permissions.AllowAny,
        # 'password_reset_confirm': permissions.AllowAny
    }

    @action(methods=['get'], filter_backends=[], detail=False)
    def my(self, request):
        queryset = User.objects.filter(id=request.user.pk).get()
        serializer = UserFullSerializer(queryset, many=False)
        return Response(serializer.data)

    # @action(methods=['post'], detail=False)
    # def password_reset(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_200_OK)

    # @action(methods=['post'], detail=False)
    # def password_reset_confirm(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_200_OK)
