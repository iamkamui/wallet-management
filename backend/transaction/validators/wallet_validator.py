from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from transaction.services import TransactionServices


@deconstructible
class WalletValidator:
    message = "This wallet number is not valid."
    code = "invalid"

    def __init__(self, message: str | None = None, code: str | None = None) -> None:
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value: str) -> None:
        if not value or len(value) != 12:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        wallet = TransactionServices.get_wallet(value)

        if not wallet:
            raise ValidationError(self.message, code=self.code, params={"value": value})
