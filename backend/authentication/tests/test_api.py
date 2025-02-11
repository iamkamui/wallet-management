from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUserAPI(APITestCase):
    def setUp(self):
        self.endpoint = reverse("auth:user-create")
        self.payload = {
            "cpf": "13625971712",
            "email": "admin@fakemail.com",
            "password": "F@kep4sswd",
            "preferred_name": "Admin",
            "full_name": "Admin Test Wallet Management",
            "phone_number": "21976514563",
        }

    def test_create_user(self):
        response = self.client.post(self.endpoint, self.payload, format="json")
        expected_response = {
            "cpf": "13625971712",
            "email": "admin@fakemail.com",
            "preferred_name": "Admin",
            "full_name": "Admin Test Wallet Management",
            "phone_number": "+5521976514563",
        }
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid_cpf(self):
        pass

    def test_create_user_invalid_phone(self):
        self.payload["phone_number"] = "00000"
        response = self.client.post(self.endpoint, self.payload, format="json")
        expected_response = {'phone_number': ['Enter a valid phone number.']}
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_email(self):
        self.payload["email"] = "adminwrongmail.com"
        response = self.client.post(self.endpoint, self.payload, format="json")
        expected_response = {'email': ['Enter a valid email address.']}
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
