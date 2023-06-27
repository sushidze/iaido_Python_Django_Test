from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from ..models import Person

User = get_user_model()


class PersonTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.admin_username = 'admin'
        self.admin_password = 'admin123'
        self.admin_user = User.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_password,
            email='admin@example.com',
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_admin_create_person(self):
        person_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '123456789',
            'date_of_birth': date(1990, 1, 1),
            'age': 33,
            'username': 'johndoe',
            'password': 'johndoepassword',
        }
        response = self.client.post('/api/persons/', person_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 3)
        self.assertEqual(Person.objects.last().first_name, 'John')

    def test_admin_get_person_detail(self):
        person = Person.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123456789',
            date_of_birth=date(1990, 1, 1),
            age=33,
            username='johndoe',
            password='johndoepassword',
        )
        response = self.client.get(f'/api/persons/{person.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_admin_update_person(self):
        person = Person.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123456789',
            date_of_birth=date(1990, 1, 1),
            age=33,
            username='johndoe',
            password='johndoepassword',
        )
        updated_data = {
            'first_name': 'Updated John',
            'last_name': 'Updated Doe',
        }
        response = self.client.patch(f'/api/persons/{person.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person.refresh_from_db()
        self.assertEqual(person.first_name, 'Updated John')

    def test_admin_delete_person(self):
        person = Person.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123456789',
            date_of_birth=date(1990, 1, 1),
            age=33,
            username='johndoe',
            password='johndoepassword',
        )
        response = self.client.delete(f'/api/persons/{person.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 2)

    def test_admin_get_person_list(self):
        response = self.client.get('/api/persons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Person.objects.count())

    def test_anybody_get_filtered_person_list(self):
        self.client.logout()
        response = self.client.get('/api/persons/filtered_persons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Person.objects.count())

    def test_guest_not_create_person(self):
        person_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '123456789',
            'date_of_birth': date(1990, 1, 1),
            'age': 33,
            'username': 'johndoe',
            'password': 'johndoepassword',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/persons/', person_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Person.objects.count(), 2)

    def test_guest_not_get_person_detail(self):
        person = Person.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123456789',
            date_of_birth=date(1990, 1, 1),
            age=33,
            username='johndoe',
            password='johndoepassword',
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/persons/{person.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_guest_not_update_person(self):
        person = Person.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123456789',
            date_of_birth=date(1990, 1, 1),
            age=33,
            username='johndoe',
            password='johndoepassword',
        )
        updated_data = {
            'first_name': 'Updated John',
            'last_name': 'Updated Doe',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/persons/{person.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_guest_not_delete_person(self):
        person = Person.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123456789',
            date_of_birth=date(1990, 1, 1),
            age=33,
            username='johndoe',
            password='johndoepassword',
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/persons/{person.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Person.objects.count(), 3)

    def test_guest_not_get_person_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/persons/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
