from cognitive.api.v1.permissions import AdminPermissions, ClientPermissions, ManagerPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from cognitive.apps.organization.models import Organization
from cognitive.apps.user.models import User
from cognitive.apps.transaction.models import Transaction


class Statistic(APIView):

    permission_classes = (AdminPermissions | ManagerPermissions | ClientPermissions)

    def get(self, request):
        data = {}
        user = self.context['request'].user

        if user.role == User.Role.ADMINISTRATOR:
            organizations = Organization.objects.non_deleted().count()
            users = User.objects.count()
            transactions = Transaction.objects.count()
            data = {
                'organizations': organizations,
                'users': users,
                'transactions': transactions,
            }

        elif user.role == User.Role.MANAGER:
            organizations = Organization.objects.non_deleted().filter(pk__in=[user.organization])
            users = User.objects.filter(organization__pk__in=[user.organization])
            transactions = Transaction.objects.filter(organization__users__exact=self.request.user.pk)
            data = {
                'organizations': organizations.count(),
                'users': users.count(),
                'transactions': transactions.count(),
            }

        elif user.role == User.Role.CLIENT:
            transactions = Transaction.objects.filter(organization__users__exact=self.request.user.pk)
            data = {
                'transactions': transactions.count(),
            }

        return Response(data)
