from cognitive.api.v1.permissions import AdminPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from cognitive.apps.organization.models import Organization
from cognitive.apps.user.models import User
from cognitive.apps.transaction.models import Transaction


class Statistic(APIView):

    permission_classes = [AdminPermissions]

    def get(self, request):
        organizations = Organization.objects.count()
        users = User.objects.count()
        transactions = Transaction.objects.count()
        data = {
            'organizations': organizations,
            'users': users,
            'transactions': transactions,
        }
        return Response(data)
