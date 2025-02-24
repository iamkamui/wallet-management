import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class CPFValidator:
    message = "Enter a valid CPF number."
    code = "invalid"
    filter_regex = r"[^0-9]"

    def __init__(self, message: str | None = None, code: str | None = None) -> None:
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value: str) -> None:
        if not value:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        cpf = re.sub(self.filter_regex, "", value)

        if not cpf or len(cpf) != 11 or cpf in [str(i) * 11 for i in range(10)]:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        first_nine = cpf[:-2]

        first_digit = self.get_valid_digit(first_nine)
        second_digit = self.get_valid_digit(first_nine + first_digit)

        valid_cpf = f"{first_nine}{first_digit}{second_digit}"

        if cpf != valid_cpf:
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def get_valid_digit(self, digits: str) -> str:
        if len(digits) not in (9, 10):
            raise ValidationError(self.message, code=self.code)

        sum_digit_multiplier = sum(
            int(digit) * multiplier for digit, multiplier in zip(digits, range(len(digits) + 1, 1, -1))
        )

        return "0" if sum_digit_multiplier % 11 < 2 else str(11 - (sum_digit_multiplier % 11))
