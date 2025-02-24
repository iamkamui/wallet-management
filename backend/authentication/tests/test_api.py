from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUserAPI(APITestCase):
    def setUp(self):
        self.endpoint = reverse("auth:user-create")
        self.payload = {
            "cpf": "11144477735",
            "email": "admin@fakemail.com",
            "password": "F@kep4sswd",
            "preferred_name": "Admin",
            "full_name": "Admin Test Wallet Management",
            "phone_number": "21976514563",
        }

    def test_create_user_return_201(self):
        response = self.client.post(self.endpoint, self.payload, format="json")
        expected_response = {
            "cpf": "11144477735",
            "email": "admin@fakemail.com",
            "preferred_name": "Admin",
            "full_name": "Admin Test Wallet Management",
            "phone_number": "+5521976514563",
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_response)

    def test_create_user_invalid_cpf_return_400(self):
        self.payload["cpf"] = "00000000000"
        response = self.client.post(self.endpoint, self.payload, format="json")
        expected_response = {"cpf": ["Enter a valid CPF number."]}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)
        
        self.payload["cpf"] = "11144477712"
        response = self.client.post(self.endpoint, self.payload, format="json")
        expected_response = {"cpf": ["Enter a valid CPF number."]}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_create_user_invalid_phone_return_400(self):
        self.payload["phone_number"] = "00000"
        response = self.client.post(self.endpoint, self.payload, format="json")
        expected_response = {"phone_number": ["Enter a valid phone number."]}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_create_user_invalid_email_return_400(self):
        self.payload["email"] = "adminwrongmail.com"
        response = self.client.post(self.endpoint, self.payload, format="json")
        expected_response = {"email": ["Enter a valid email address."]}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)
