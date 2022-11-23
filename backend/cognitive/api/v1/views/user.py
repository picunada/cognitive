from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from cognitive.api.v1.permissions import AdminPermissions, ManagerPermissions, ClientPermissions
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
    ordering_fields = ('id',)
    search_fields = ('first_name', 'last_name')

    serializer_class_map = {
        'create': UserCreateUpdateSerializer,
        'update': UserCreateUpdateSerializer,
        'partial_update': UserCreateUpdateSerializer,
        # 'password_reset': PasswordResetSerializer,
        # 'password_reset_confirm': PasswordResetConfirmSerializer
    }

    permission_map = {
        'create': (AdminPermissions | ManagerPermissions),
        'list': (AdminPermissions | ManagerPermissions),
        'update': (AdminPermissions | ManagerPermissions),
        'partial_update': (AdminPermissions | ManagerPermissions),
        'destroy': (AdminPermissions | ManagerPermissions),
        'my': permissions.IsAuthenticated,
        # 'password_reset': permissions.AllowAny,
        # 'password_reset_confirm': permissions.AllowAny
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if AdminPermissions().has_permission(self.request, self):
            return queryset
        if ManagerPermissions().has_permission(self.request, self):
            queryset = queryset.filter(role=User.Role.CLIENT)

        return queryset.distinct()

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        if user.role != User.Role.ADMINISTRATOR and not all(elem in user.organization.all() for elem in instance.organization.all()):
            return Response({'role': ['not enough permissions']}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
