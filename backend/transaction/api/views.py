from django.core.exceptions import ValidationError
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from transaction.api.permissions import IsWalletOwner
from transaction.api.serializers import TransactionFilterSerializer, TransactionSerializer, WalletSerializer
from transaction.services import TransactionServices


class TransactionViewSet(viewsets.ViewSet):
    serializer_class = TransactionSerializer
    filter_serializer_class = TransactionFilterSerializer
    wallet_serializer_class = WalletSerializer
    service = TransactionServices

    @action(
        methods=["get"],
        detail=False,
        url_name="check-balance",
        url_path="check_balance",
        permission_classes=[IsAuthenticated, IsWalletOwner],
    )
    def check_balance(self, request: Request) -> Response:
        wallet_serializer = WalletSerializer(data=request.query_params)
        wallet_serializer.is_valid(raise_exception=True)
        wallet_pk = wallet_serializer.validated_data["wallet"]

        wallet = self.service.get_wallet(wallet_pk)

        response_data = WalletSerializer(wallet).data

        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, url_name="deposit", url_path="deposit", permission_classes=[AllowAny])
    def deposit(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if "from_wallet" in serializer.validated_data:
            raise exceptions.ParseError(
                "Field 'from_wallet' is not allowed on deposit. Use /transfer endpoint to transfer beetween wallets",
                code="invalid_field",
            )

        _data = {
            "user": request.user,
            "to_wallet": self.service.get_wallet(serializer.validated_data["to_wallet"]),
            "amount": serializer.validated_data["amount"],
        }

        service = self.service(**_data)
        try:
            deposit_transaction = service.deposit()
        except ValidationError as exc:
            return Response(data=exc, status=status.HTTP_400_BAD_REQUEST)

        transaction_serializer = self.serializer_class(deposit_transaction)
        response_data = transaction_serializer.data
        del response_data["to_wallet"]["balance"]

        return Response(data=transaction_serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, permission_classes=[IsAuthenticated, IsWalletOwner])
    def transfer(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        from_wallet = self.service.get_wallet(serializer.validated_data["from_wallet"])
        to_wallet = self.service.get_wallet(serializer.validated_data["to_wallet"])
        amount = serializer.validated_data["amount"]

        service = self.service(user, to_wallet, from_wallet, amount)  # type: ignore

        try:
            transfer_transaction = service.transfer()
        except ValidationError as exc:
            return Response(data=exc, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = self.serializer_class(transfer_transaction)

        response_data = response_serializer.data
        del response_data["to_wallet"]["balance"]

        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated, IsWalletOwner], url_path="list")
    def transaction_list(self, request: Request) -> Response:
        filter_serializer = self.filter_serializer_class(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        transactions = self.service.transaction_list(filter_serializer.validated_data)
        serializer = self.serializer_class(transactions, many=True)
        for transaction in serializer.data:
            del transaction["to_wallet"]["balance"]
            if "from_wallet" in transaction and transaction["from_wallet"] is not None:
                del transaction["from_wallet"]["balance"]
        return Response(data=serializer.data, status=status.HTTP_200_OK)
