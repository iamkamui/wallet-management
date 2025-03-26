from decimal import Decimal

from authentication.models import User
from django.core.exceptions import ValidationError

from transaction.enums import TransactionStatus
from transaction.models import Transaction, Wallet


class TransactionServices:
    def __init__(self, user: User, to_wallet: Wallet, from_wallet: Wallet | None = None, amount: int = 0) -> None:
        self.user = user
        self.from_wallet = from_wallet
        self.to_wallet = to_wallet
        self.amount = amount
        self.transaction = self._create_transaction(self.user, self.to_wallet, self.from_wallet, self.amount)

    def _create_transaction(
        self, user: User, to_wallet: Wallet, from_wallet: Wallet | None = None, amount: int = 0
    ) -> Transaction:
        transaction_data = {"from_wallet": from_wallet, "to_wallet": to_wallet, "amount": amount, "requested_by": user}

        if not from_wallet:
            del transaction_data["from_wallet"]

        transaction = Transaction.objects.create(**transaction_data)
        return transaction

    @staticmethod
    def get_wallet(wallet_pk: str) -> Wallet | None:
        try:
            wallet = Wallet.objects.get(pk=wallet_pk)
        except Wallet.DoesNotExist:
            return None
        return wallet

    def deposit(self) -> Transaction:
        previous_balance = self.transaction.to_wallet.balance

        if self.amount <= 0:
            self.transaction.status = TransactionStatus.FAILURE
            self.transaction.save()
            raise ValidationError("The amount value can not be less or equal 0")

        new_wallet_balance = previous_balance + self.transaction.amount
        try:
            self.transaction.to_wallet.balance = Decimal(new_wallet_balance).quantize(Decimal("0.01"))
            self.transaction.to_wallet.full_clean()
            self.transaction.to_wallet.save()
            self.transaction.full_clean()
            self.transaction.status = TransactionStatus.SETTLED
            self.transaction.save()
        except ValidationError:
            self.transaction.status = TransactionStatus.FAILURE
            self.transaction.save()
        return self.transaction
