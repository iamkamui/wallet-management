from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from transaction.services import TransactionServices


class IsAdminOrWalletOwner(BasePermission):  # type: ignore
    service = TransactionServices
    message = "You are not the owner of this wallet."

    def has_permission(self, request: Request, view: APIView) -> bool:
        wallet_pk = view.kwargs.get("pk") or request.data["to_wallet"]["number"]
        if not wallet_pk:
            return False

        if request.user and request.user.is_staff:
            return True

        wallet = self.service.get_wallet(wallet_pk=wallet_pk)
        return bool(wallet.user == request.user) if wallet else False
