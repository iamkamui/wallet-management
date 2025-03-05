from authentication.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from transaction.models import Wallet


class TestTransactionAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            **{
                "cpf": "11144477735",
                "email": "admin@fakemail.com",
                "password": "F@kep4sswd",
                "preferred_name": "Admin",
                "full_name": "Admin Test Wallet Management",
                "phone_number": "21976514563",
            }
        )
        cls.wallet = Wallet.objects.create(user=cls.test_user, balance=100)
        cls.test_user2 = User.objects.create_user(
            **{
                "cpf": "88517476794",
                "email": "admin2@fakemail.com",
                "password": "F@kep4sswd",
                "preferred_name": "Admin2",
                "full_name": "Admin2 Test Wallet Management",
                "phone_number": "21995108165",
            }
        )
        cls.wallet2 = Wallet.objects.create(user=cls.test_user2, balance=150)
        cls.balance_endpoint = reverse("wallet:transaction-check-balance", kwargs={"pk": cls.wallet.number})
        cls.balance2_endpoint = reverse("wallet:transaction-check-balance", kwargs={"pk": cls.wallet2.number})

    def test_check_balance_unauthenticated_user_returns_401(self):
        response = self.client.get(self.balance_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_balance_authenticated_non_owner_returns_403(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.balance2_endpoint)
        expected_response = {"detail": "You are not the owner of this wallet."}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_check_balance_authenticated_owner_returns_200(self):
        self.client.force_authenticate(user=self.test_user2)
        response = self.client.get(self.balance2_endpoint)
        expected_response = {'number': self.wallet2.pk, 'balance': '150.00'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)
