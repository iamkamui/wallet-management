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
    created_at = serializers.DateTimeField(read_only=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        view = self.context.get("view")
        if view and view.action == "transfer":
            self.from_wallet.required = True


class TransactionFilterSerializer(serializers.Serializer[Transaction]):
    wallet = serializers.CharField(required=True, validators=[WalletValidator()])
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
