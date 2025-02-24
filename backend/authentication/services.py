from phonenumber_field.phonenumber import PhoneNumber

from authentication.models import User


class UserServices:
    def __init__(self, user: User):
        self.user = user

    @classmethod
    def create_user(
        cls, cpf: str, email: str, password: str, preferred_name: str, full_name: str, phone_number: PhoneNumber
    ) -> User:
        user = User.objects.create_user(
            cpf=cpf,
            email=email,
            password=password,
            preferred_name=preferred_name,
            full_name=full_name,
            phone_number=phone_number,
        )
        return user
