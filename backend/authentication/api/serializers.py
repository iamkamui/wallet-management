from typing import Any

from phonenumber_field import serializerfields
from rest_framework import serializers
from transaction.api.serializers import WalletSerializer

from authentication.models import Profile, User
from authentication.validators import CPFValidator


class ProfileSerializer(serializers.Serializer[Profile]):
    preferred_name = serializers.CharField(max_length=50, required=True)
    full_name = serializers.CharField(max_length=254, required=True)
    phone_number = serializerfields.PhoneNumberField(required=True)


class UserSerializer(serializers.Serializer[User]):
    cpf = serializers.CharField(max_length=11, required=True, validators=[CPFValidator()])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    preferred_name = serializers.CharField(max_length=50, required=True, write_only=True)
    full_name = serializers.CharField(max_length=254, required=True, write_only=True)
    phone_number = serializerfields.PhoneNumberField(required=True, write_only=True)
    profile = ProfileSerializer(read_only=True)

    def to_representation(self, instance: User) -> dict[str, Any]:
        wallets = instance.wallet_set.all()
        ret = super().to_representation(instance)
        if wallets:
            ret["wallets"] = WalletSerializer(wallets, many=True).data  # type: ignore
        return ret
