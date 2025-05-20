from typing import Any

from django.db import IntegrityError, transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.api.serializers import UserSerializer
from authentication.services import UserServices

__all__ = ("UserViewSet",)

ALLOW_ANY_ACTIONS = ["create_user"]


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    service = UserServices
    permission_classes = [IsAuthenticated]

    def get_permissions(self) -> list[Any]:
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ALLOW_ANY_ACTIONS:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    @action(methods=["post"], detail=False, url_name="create", url_path="create")
    def create_user(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cpf = serializer.validated_data["cpf"]
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            preferred_name = serializer.validated_data["preferred_name"]
            full_name = serializer.validated_data["full_name"]
            phone_number = serializer.validated_data["phone_number"]

            with transaction.atomic():
                user = self.service.create_user(cpf, email, password)
                user_service = self.service(user)
                user_service.create_profile(preferred_name, full_name, phone_number)
                user_service.create_wallet()
        except IntegrityError as exp:
            return Response(data=str(exp), status=status.HTTP_400_BAD_REQUEST)

        response_data = self.serializer_class(user).data
        return Response(data=response_data, status=status.HTTP_201_CREATED)
