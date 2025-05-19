from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from transaction.services import TransactionServices


class IsWalletOwner(BasePermission):
    service = TransactionServices
    message = "You are not the owner of this wallet."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if isinstance(request.user, AnonymousUser):
            return False

        if request.method == "GET":
            wallet_pk = request.query_params["wallet"]

        if request.method == "POST":
            if isinstance(request.data, dict) and "wallet" in request.data:
                wallet_pk = request.data["wallet"]["number"]

            if isinstance(request.data, dict) and "from_wallet" in request.data:
                wallet_pk = request.data["from_wallet"]["number"]

        wallet = self.service.get_wallet(wallet_pk=wallet_pk)
        return bool(wallet.user == request.user) if wallet else False
