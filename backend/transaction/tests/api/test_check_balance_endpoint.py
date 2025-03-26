from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from transaction.tests.factories import WalletFactory


class TestCheckBalanceEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.wallet = WalletFactory.create(balance=100)
        cls.wallet2 = WalletFactory.create(balance=150)

    def test_check_balance_unauthenticated_user_returns_401(self):
        endpoint = reverse("transaction:wallet-check-balance", kwargs={"pk": self.wallet.number})
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_balance_authenticated_non_owner_returns_403(self):
        self.client.force_authenticate(user=self.wallet.user)
        endpoint = reverse("transaction:wallet-check-balance", kwargs={"pk": self.wallet2.number})
        response = self.client.get(endpoint)
        expected_response = {"detail": "You are not the owner of this wallet."}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_check_balance_authenticated_owner_returns_200(self):
        self.client.force_authenticate(user=self.wallet2.user)
        endpoint = reverse("transaction:wallet-check-balance", kwargs={"pk": self.wallet2.number})
        response = self.client.get(endpoint)
        expected_response = {"number": self.wallet2.pk, "balance": "150.00"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)
