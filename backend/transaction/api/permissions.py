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
            wallet_pk = request.data.get("wallet") or request.data.get("from_wallet")  # type: ignore

        if not wallet_pk:
            return False

        wallet = self.service.get_wallet(wallet_pk=wallet_pk)
        return bool(wallet.user == request.user) if wallet else False
