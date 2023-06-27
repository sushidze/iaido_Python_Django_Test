from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AgeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_username = 'admin'
        self.admin_password = 'admin123'
        self.admin_user = User.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_password,
            email='admin@example.com',
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_invalid_age(self):
        person_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '123456789',
            'date_of_birth': date(1990, 1, 1),
            'age': 25,  # Invalid age value
            'username': 'johndoe',
            'password': 'johndoepassword',
        }
        response = self.client.post('/api/persons/', person_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            'Invalid age. Check date of birth or age.'
        )
