from django.db import models


class TransactionStatus(models.TextChoices):
    PENDING = "001", "Pending"
    AUTHORIZED = "002", "Authorized"
    SETTLED = "003", "Settled"
    FAILURE = "004", "Failure"
