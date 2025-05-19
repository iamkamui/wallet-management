from typing import Any

from rest_framework import serializers

from transaction.enums import TransactionStatus
from transaction.models import Transaction, Wallet
from transaction.validators import WalletValidator


class WalletSerializer(serializers.Serializer[Wallet]):
    wallet = serializers.CharField(required=True, validators=[WalletValidator()], write_only=True)
    number = serializers.CharField(read_only=True, validators=[WalletValidator()])
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, read_only=True)

    def to_representation(self, instance: Wallet) -> dict[str, Any]:
        ret = super().to_representation(instance)
        wallet_number = ret.pop("number")
        ret["wallet"] = wallet_number
        return ret


class TransactionSerializer(serializers.Serializer[Transaction]):
    from_wallet = serializers.CharField(required=False, validators=[WalletValidator()])
    to_wallet = serializers.CharField(required=True, validators=[WalletValidator()])
    amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    status = serializers.ChoiceField(choices=TransactionStatus.choices, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        view = self.context.get("view")
        if view and view.action == "transfer":
            self.from_wallet.required = True

    def to_representation(self, instance: Transaction) -> dict[str, Any]:
        to_wallet = instance.to_wallet
        from_wallet = instance.from_wallet
        ret = super().to_representation(instance)
        if to_wallet and isinstance(to_wallet, Wallet):
            ret["to_wallet"] = WalletSerializer(to_wallet).data

        if from_wallet and isinstance(from_wallet, Wallet):
            ret["from_wallet"] = WalletSerializer(from_wallet).data
        return ret


class TransactionFilterSerializer(serializers.Serializer[Transaction]):
    wallet = serializers.CharField(required=True, validators=[WalletValidator()])
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
