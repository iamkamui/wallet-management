from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from transaction.tests.factories import WalletFactory


class TestTransferEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.from_wallet = WalletFactory.create(balance=1000)
        cls.to_wallet = WalletFactory.create()
        cls.endpoint = reverse("transaction:wallet-transfer")

    def test_transfer_authenticated_without_from_wallet_return_403(self):
        self.client.force_authenticate(user=self.from_wallet.user)

        payload = {"amount": 500, "to_wallet": {"number": self.to_wallet.pk}, "from_wallet": {"number": None}}
        response = self.client.post(self.endpoint, payload, format="json")

        expected_response = "You are not the owner of this wallet."

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], expected_response)

    def test_transfer_authenticated_without_be_wallet_owner_return_403(self):
        """if i'm authenticated with a user, i have to be permitted to transfer balance only from my own wallets."""
        self.client.force_authenticate(user=self.to_wallet.user)

        payload = {
            "amount": 500,
            "to_wallet": {"number": self.to_wallet.pk},
            "from_wallet": {"number": self.from_wallet.pk},
        }
        response = self.client.post(self.endpoint, payload, format="json")

        expected_response = "You are not the owner of this wallet."

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], expected_response)

    def test_transfer_without_enouth_balance_return_400(self):
        self.client.force_authenticate(user=self.from_wallet.user)

        payload = {
            "amount": 1500,
            "to_wallet": {"number": self.to_wallet.pk},
            "from_wallet": {"number": self.from_wallet.pk},
        }
        response = self.client.post(self.endpoint, payload, format="json")

        expected_response = "Not enouth balance on wallet to transfer"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], expected_response)

    def test_transfer_to_invalid_wallet_return_400(self):
        self.client.force_authenticate(user=self.from_wallet.user)

        payload = {
            "amount": 1500,
            "to_wallet": {"number": "000000000012"},
            "from_wallet": {"number": self.from_wallet.pk},
        }
        response = self.client.post(self.endpoint, payload, format="json")

        expected_response = {"to_wallet": {"number": ["This wallet number is not valid."]}}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_transfer_0_amount_return_400(self):
        self.client.force_authenticate(user=self.from_wallet.user)

        payload = {
            "amount": 0,
            "to_wallet": {"number": self.to_wallet.pk},
            "from_wallet": {"number": self.from_wallet.pk},
        }
        response = self.client.post(self.endpoint, payload, format="json")

        expected_response = "The amount value can not be less or equal 0"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], expected_response)

    def test_transfer_200_into_wallets_return_200(self):
        self.client.force_authenticate(user=self.from_wallet.user)

        payload = {
            "amount": 200,
            "to_wallet": {"number": self.to_wallet.pk},
            "from_wallet": {"number": self.from_wallet.pk},
        }

        response = self.client.post(self.endpoint, payload, format="json")
        response_data = response.json()

        expected_response = {
            "from_wallet": {"number": self.from_wallet.pk, "balance": "800.00"},
            "to_wallet": {"number": self.to_wallet.pk},
            "amount": "200.00",
            "status": "003",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["from_wallet"], expected_response["from_wallet"])
        self.assertEqual(response_data["to_wallet"], expected_response["to_wallet"])
        self.assertEqual(response_data["amount"], expected_response["amount"])
        self.assertEqual(response_data["status"], expected_response["status"])
        self.assertIn("created_at", response_data)
