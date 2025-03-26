import re

import factory
from authentication.models import Profile, User
from wallet_management.utils.tests.base import faker

from transaction.models import Transaction, Wallet


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    preferred_name = factory.LazyAttribute(lambda _self: _self.full_name.split(" ")[0])
    full_name = factory.LazyAttribute(lambda _: faker.name())
    phone_number = factory.LazyAttribute(lambda _: faker.cellphone_number())
    user = factory.SubFactory("transaction.tests.factories.UserFactory")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: faker.unique.free_email())
    cpf = factory.LazyAttribute(lambda _: re.sub(r"[^0-9]", "", faker.cpf()))
    profile = factory.RelatedFactory(ProfileFactory, "user")

    class Params:
        is_admin = factory.Trait(is_staff=True)


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    number = factory.LazyAttribute(lambda _self: Wallet.generate_wallet_number(_self.user))
    user = factory.SubFactory(UserFactory)
    balance = factory.LazyAttribute(
        lambda _: faker.pyfloat(positive=True, left_digits=faker.pyint(max_value=8), right_digits=2, min_value=0.1)
    )


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    to_wallet = factory.SubFactory(WalletFactory)
    amount = factory.LazyAttribute(
        lambda _: faker.pyfloat(positive=True, left_digits=faker.pyint(max_value=8), right_digits=2, min_value=0.1)
    )
    requested_by = factory.SubFactory(UserFactory)

    class Params:
        with_from_wallet = factory.Trait(from_wallet=factory.SubFactory(WalletFactory))
