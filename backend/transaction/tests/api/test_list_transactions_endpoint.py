from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from transaction.enums import TransactionStatus
from transaction.tests.factories import TransactionFactory, UserFactory, WalletFactory, faker


class TestTransactionListEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.wallet = WalletFactory.create(user=cls.user)
        cls.endpoint = reverse("transaction:wallet-transaction-list")

        for _ in range(5):
            TransactionFactory.create(to_wallet=cls.wallet, with_from_wallet=True, status=TransactionStatus.SETTLED)
            TransactionFactory.create(from_wallet=cls.wallet, requested_by=cls.user, status=TransactionStatus.SETTLED)
            TransactionFactory.create()

    def test_list_transaction_without_date_reange_return_all(self):
        self.client.force_authenticate(user=self.user)
        payload = {"wallet": self.wallet.pk}
        response = self.client.get(self.endpoint, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 10)


        for transaction in response.json():
            self.assertTrue(
                transaction["from_wallet"]["wallet"] == self.wallet.pk
                or transaction["to_wallet"]["wallet"] == self.wallet.pk
            )

    def test_list_transaction_with_date_range_return_only_in_range(self):
        self.client.force_authenticate(user=self.user)

        year = timezone.localtime().year - 1
        start_date = timezone.localtime().replace(day=1, month=1, hour=0, year=year)
        end_date = timezone.localtime().replace(day=31, month=12, hour=0, year=year)

        for _ in range(5):
            created_at = faker.date_time_between_dates(start_date, end_date, tzinfo=timezone.get_current_timezone())
            TransactionFactory.create(
                to_wallet=self.wallet,
                with_from_wallet=True,
                status=TransactionStatus.SETTLED,
                created_at=created_at,
            )

        payload = {"wallet": self.wallet.pk, "start_date": start_date.date(), "end_date": end_date.date()}

        response = self.client.get(self.endpoint, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 5)

        for transaction in response.json():
            self.assertTrue(
                transaction["from_wallet"]["wallet"] == self.wallet.pk
                or transaction["to_wallet"]["wallet"] == self.wallet.pk
            )

    def test_list_transaction_unauthenticated_return_401(self):
        payload = {"wallet": self.wallet.pk}
        response = self.client.get(self.endpoint, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_transaction_authenticated_without_be_wallet_owner_return_403(self):
        self.client.force_authenticate(user=self.user)
        payload = {"wallet": WalletFactory.create().pk}
        response = self.client.get(self.endpoint, payload, format="json")

        expected_response = {"detail": "You are not the owner of this wallet."}

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(expected_response, response.json())
