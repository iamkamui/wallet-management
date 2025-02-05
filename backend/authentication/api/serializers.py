from phonenumber_field import serializerfields
from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.Serializer[User]):
    cpf = serializers.CharField(max_length=11, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    preferred_name = serializers.CharField(max_length=50, required=True)
    full_name = serializers.CharField(max_length=254, required=True)
    phone_number = serializerfields.PhoneNumberField(required=True)
