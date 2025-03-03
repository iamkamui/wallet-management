from rest_framework import serializers

from transaction.models import Wallet


class WalletSerializer(serializers.Serializer[Wallet]):
    number = serializers.CharField(required=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
