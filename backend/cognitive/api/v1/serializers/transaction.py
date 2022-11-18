from rest_framework import serializers
from cognitive.apps.transaction.models import Transaction


class TransactionFullSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'organization', 'created_at', 'deleted_at')
        read_only_fields = ('id', 'created_at')
        model = Transaction
