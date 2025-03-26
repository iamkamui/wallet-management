from django.urls import reverse
from rest_framework.test import APITestCase

from transaction.tests.factories import WalletFactory


class TestDepositEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.wallet = WalletFactory.create()
        cls.payload = {"to_wallet": {"number": cls.wallet.pk}}
        cls.endpoint = reverse("transaction:wallet-deposit")

    def test_deposit_positive_amount_updates_wallet_balance_return_200(self):
        self.client.force_authenticate(user=self.wallet.user)

        expected_response = {
            "from_wallet": None,
            "to_wallet": {"number": self.wallet.pk},
            "amount": "500.00",
            "status": "003",
        }
        self.payload["amount"] = 500.00
        response = self.client.post(self.endpoint, self.payload, format="json")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), expected_response)

    def test_deposit_negative_amount_raise_validation_error_400(self):
        self.client.force_authenticate(user=self.wallet.user)

        expected_response = "The amount value can not be less or equal 0"
        self.payload["amount"] = -500.00
        response = self.client.post(self.endpoint, self.payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], expected_response)

    def test_deposit_zero_raise_validation_error_400(self):
        self.client.force_authenticate(user=self.wallet.user)

        expected_response = "The amount value can not be less or equal 0"
        self.payload["amount"] = 0
        response = self.client.post(self.endpoint, self.payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], expected_response)
