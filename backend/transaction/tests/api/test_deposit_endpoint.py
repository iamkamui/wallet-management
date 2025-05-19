from django.urls import reverse
from rest_framework.test import APITestCase

from transaction.tests.factories import UserFactory, WalletFactory


class TestDepositEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.wallet = WalletFactory.create(user=cls.user)
        cls.endpoint = reverse("transaction:wallet-deposit")

    def test_deposit_positive_amount_updates_wallet_balance_return_200(self):
        self.client.force_authenticate(user=self.wallet.user)
        payload = {"to_wallet": {"number": self.wallet.pk}, "amount": 500}

        expected_response = {
            "from_wallet": None,
            "to_wallet": {"number": self.wallet.pk},
            "amount": "500.00",
            "status": "003",
        }
        response = self.client.post(self.endpoint, payload, format="json")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["from_wallet"], response_data["from_wallet"])
        self.assertEqual(expected_response["to_wallet"], response_data["to_wallet"])
        self.assertEqual(expected_response["amount"], response_data["amount"])
        self.assertEqual(expected_response["status"], response_data["status"])
        self.assertIn("created_at", response_data)

    def test_deposit_negative_amount_raise_validation_error_400(self):
        self.client.force_authenticate(user=self.wallet.user)
        payload = {"to_wallet": {"number": self.wallet.pk}, "amount": -500}

        expected_response = "The amount value can not be less or equal 0"
        response = self.client.post(self.endpoint, payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], expected_response)

    def test_deposit_zero_raise_validation_error_400(self):
        self.client.force_authenticate(user=self.wallet.user)
        payload = {"to_wallet": {"number": self.wallet.pk}, "amount": 0}

        expected_response = "The amount value can not be less or equal 0"
        response = self.client.post(self.endpoint, payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], expected_response)

    def test_deposit_with_from_wallet_return_400(self):
        self.client.force_authenticate(user=self.wallet.user)
        payload = {"from_wallet": {"number": self.wallet.pk}, "to_wallet": {"number": self.wallet.pk}, "amount": 500}
        response = self.client.post(self.endpoint, payload, format="json")
        expected_response = {
            "detail": "Field 'from_wallet' is not allowed on deposit. Use /transfer endpoint to transfer beetween wallets"  # noqa: E501
        }
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_response)
