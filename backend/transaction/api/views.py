from django.core.exceptions import ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from transaction.api.permissions import IsAdminOrWalletOwner
from transaction.api.serializers import TransactionSerializer, WalletSerializer
from transaction.models import Transaction
from transaction.services import TransactionServices


class TransactionViewSet(viewsets.ViewSet):
    serializer_class = TransactionSerializer
    wallet_serializer_class = WalletSerializer
    service = TransactionServices
    permission_classes = [IsAuthenticated, IsAdminOrWalletOwner]

    @action(methods=["get"], detail=True, url_name="check-balance", url_path="check_balance")
    def check_balance(self, request: Request, pk: str) -> Response:
        wallet = self.service.get_wallet(pk)

        wallet_serializer = self.wallet_serializer_class(wallet)

        return Response(data=wallet_serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, url_name="deposit", url_path="deposit")
    def deposit(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        _data = {
            "user": request.user,
            "to_wallet": self.service.get_wallet(serializer.validated_data["to_wallet"]["number"]),
            "amount": serializer.validated_data["amount"],
        }

        if hasattr(serializer.validated_data, "from_wallet"):
            _data.update({"from_wallet": self.service.get_wallet(serializer.validated_data["from_wallet"]["number"])})

        service = self.service(**_data)  # type: ignore
        try:
            deposit_transaction = service.deposit()
        except ValidationError as exc:
            return Response(data=exc, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            "requested_by": deposit_transaction.requested_by,
            "to_wallet": deposit_transaction.to_wallet,
            "amount": deposit_transaction.amount,
            "status": deposit_transaction.status,
        }

        if deposit_transaction.from_wallet is not None:
            response_data.update({"from_wallet": {"number": deposit_transaction.from_wallet.pk}})

        transaction_serializer = self.serializer_class(Transaction(**response_data))

        return Response(data=transaction_serializer.data, status=status.HTTP_200_OK)
