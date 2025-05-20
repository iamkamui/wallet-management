from phonenumber_field.phonenumber import PhoneNumber
from transaction.models import Wallet

from authentication.models import Profile, User


class UserServices:
    def __init__(self, user: User):
        self.user = user

    def create_profile(self, preferred_name: str, full_name: str, phone_number: PhoneNumber) -> Profile:
        profile = Profile(preferred_name=preferred_name, full_name=full_name, phone_number=phone_number, user=self.user)
        profile.full_clean()
        profile.save()
        return profile

    def create_wallet(self) -> Wallet:
        wallet = Wallet(user=self.user)
        wallet.full_clean(exclude={"number"})
        wallet.save()
        return wallet

    @classmethod
    def create_user(cls, cpf: str, email: str, password: str) -> User:
        user = User.objects.create_user(cpf=cpf, email=email, password=password)
        return user
