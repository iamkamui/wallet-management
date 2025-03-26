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
        time = str(timezone.now().strftime("%M%S"))
        day_and_month = str(timezone.now().strftime("%-m%-d"))
        year = str(timezone.now().strftime("%y"))
        lenght_diference = 12 - len(time + day_and_month + year)
        user_cpf_last_digits = user.cpf.replace("-", "")[-lenght_diference:]

        wallet_number = f"{year}{time}{day_and_month}{user_cpf_last_digits}"
        return wallet_number


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

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=TransactionStatus.values),
            )
        ]
