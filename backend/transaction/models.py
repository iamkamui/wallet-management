from typing import Any

from authentication.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from transaction.enums import TransactionStatus


class Wallet(models.Model):
    number = models.CharField("wallet number", max_length=12, validators=[MinLengthValidator(12)], primary_key=True)
    user = models.ForeignKey(User, verbose_name="owner", on_delete=models.CASCADE)
    balance = models.DecimalField("wallet balance", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("date joined", default=timezone.now)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.number:
            self.number = self.generate_wallet_number(self.user)
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_wallet_number(user: User) -> str:
        wallet_max_length = 12
        year = str(timezone.now().strftime("%y"))
        timestamp = str(timezone.now().timestamp()).replace(".", "")
        lenght_diference = wallet_max_length - len(timestamp)
        user_cpf_last_digits = user.cpf.replace("-", "")[-lenght_diference:]

        wallet_number = f"{year}{user_cpf_last_digits}{timestamp}"

        return wallet_number[:wallet_max_length]


class Transaction(models.Model):
    from_wallet = models.ForeignKey(
        Wallet,
        verbose_name="origin wallet",
        on_delete=models.CASCADE,
        related_name="sent_transactions",
        null=True,
        blank=True,
    )
    to_wallet = models.ForeignKey(
        Wallet,
        verbose_name="destination wallet",
        on_delete=models.CASCADE,
        related_name="received_transactions",
        null=False,
    )
    amount = models.DecimalField("transaction amount", max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        "transaction status", max_length=3, choices=TransactionStatus, default=TransactionStatus.PENDING
    )
    requested_by = models.ForeignKey(User, verbose_name="who realized", on_delete=models.CASCADE)
    created_at = models.DateTimeField("date joined", default=timezone.now)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                condition=models.Q(status__in=TransactionStatus.values),
            )
        ]
