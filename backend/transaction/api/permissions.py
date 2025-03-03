from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from transaction.services import TransactionServices


class IsWalletOwner(BasePermission):  # type: ignore
    service = TransactionServices

    def has_permission(self, request: Request, view: APIView) -> bool:
        wallet_pk = view.kwargs.get("pk")
        if not wallet_pk:
            return False

        wallet = self.service.get_wallet(wallet_pk=wallet_pk)
        return bool(wallet.user == request.user) if wallet else False
