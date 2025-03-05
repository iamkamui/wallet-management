from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from transaction.api.permissions import IsWalletOwner
from transaction.api.serializers import WalletSerializer
from transaction.services import TransactionServices


class TransactionViewSet(viewsets.ViewSet):
    # serializer_class = TransactionSerializer
    wallet_serializer_class = WalletSerializer
    service = TransactionServices
    permission_classes = [IsAuthenticated]

    @action(
        methods=["get"],
        detail=True,
        url_name="check-balance",
        url_path="check_balance",
        permission_classes=[IsAuthenticated, IsWalletOwner],
    )
    def check_balance(self, request: Request, pk: str) -> Response:
        wallet = self.service.get_wallet(pk)

        wallet_serializer = self.wallet_serializer_class(wallet)

        return Response(data=wallet_serializer.data, status=status.HTTP_200_OK)
