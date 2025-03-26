from typing import Any

from rest_framework import serializers

from transaction.enums import TransactionStatus
from transaction.models import Transaction, Wallet
from transaction.validators import WalletValidator


class WalletSerializer(serializers.Serializer[Wallet]):
    number = serializers.CharField(required=True, validators=[WalletValidator()])
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class TransactionSerializer(serializers.Serializer[Transaction]):
    from_wallet = WalletSerializer(required=False)
    to_wallet = WalletSerializer(required=True)
    amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    status = serializers.ChoiceField(choices=TransactionStatus.choices, read_only=True)

    def to_representation(self, instance: Transaction) -> Any:
        ret = super().to_representation(instance)
        del ret["to_wallet"]["balance"]
        return ret
