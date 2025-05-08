import unittest
from decimal import Decimal

from django.core.exceptions import ValidationError

from transaction.enums import TransactionStatus
from transaction.services import TransactionServices
from transaction.tests.factories import WalletFactory


class TestTransactionServiceDeposit(unittest.TestCase):
    def setUp(self):
        self.user_wallet = WalletFactory.create()
        self.transaction_service = TransactionServices

    def test_deposit_positive_amount_updates_wallet_balance(self):
        wallet_previous_value = self.user_wallet.balance
        service = TransactionServices(self.user_wallet.user, self.user_wallet, amount=500)

        expected_balance = Decimal(wallet_previous_value) + 500
        expected_balance = expected_balance.quantize(Decimal("0.01"))

        transaction = service.deposit()
        self.assertEqual(transaction.to_wallet.balance, expected_balance)
        self.assertEqual(transaction.status, TransactionStatus.SETTLED)

    def test_deposit_negative_amount_raise_validation_error(self):
        service = TransactionServices(self.user_wallet.user, self.user_wallet, amount=-500)

        with self.assertRaises(ValidationError) as vde:
            _ = service.deposit()

        self.assertEqual("The amount value can not be less or equal 0", vde.exception.message)

    def test_deposit_zero_raise_validation_error(self):
        service = TransactionServices(self.user_wallet.user, self.user_wallet, amount=0)

        with self.assertRaises(ValidationError) as vde:
            _ = service.deposit()

        self.assertEqual(service.transaction.status, TransactionStatus.FAILURE)
        self.assertEqual("The amount value can not be less or equal 0", vde.exception.message)


class TestTransactionServiceTransfer(unittest.TestCase):
    def setUp(self):
        self.from_wallet = WalletFactory.create(balance=1000)
        self.to_wallet = WalletFactory.create()
        self.transaction_service = TransactionServices

    def test_transfer_without_from_wallet_raises_validation_error(self):
        service = TransactionServices(self.to_wallet.user, self.to_wallet, amount=100)

        with self.assertRaises(ValidationError) as vde:
            _ = service.transfer()

        self.assertEqual(service.transaction.status, TransactionStatus.FAILURE)
        self.assertEqual("Transfer transaction can not be perform without from wallet", vde.exception.message)

    def test_transfer_without_enouth_balance_raises_validation_error(self):
        service = TransactionServices(self.to_wallet.user, self.to_wallet, self.from_wallet, 1100)

        with self.assertRaises(ValidationError) as vde:
            _ = service.transfer()

        self.assertEqual(service.transaction.status, TransactionStatus.FAILURE)
        self.assertEqual("Not enouth balance on wallet to transfer", vde.exception.message)

    def test_transfer_to_other_wallet_update_wallets_balance(self):
        to_wallet_balance = self.to_wallet.balance
        from_wallet_balance = self.from_wallet.balance

        service = TransactionServices(self.to_wallet.user, self.to_wallet, self.from_wallet, 150)
        transaction = service.transfer()

        self.assertEqual(transaction.status, TransactionStatus.SETTLED)
        self.assertEqual(service._to_wallet.balance, Decimal(to_wallet_balance + 150).quantize(Decimal("1.01")))
        self.assertEqual(service._from_wallet.balance, Decimal(from_wallet_balance - 150).quantize(Decimal("1.01")))