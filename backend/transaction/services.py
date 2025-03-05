from authentication.models import User

from transaction.models import Wallet


class TransactionServices:
    def __init__(self, user: User, from_wallet: Wallet, to_wallet: Wallet | None = None) -> None:
        self.user = user
        self.from_wallet = from_wallet
        self.to_wallet = to_wallet

    @staticmethod
    def get_wallet(wallet_pk: str) -> Wallet | None:
        try:
            wallet = Wallet.objects.get(pk=wallet_pk)
        except Wallet.DoesNotExist:
            return None
        return wallet
