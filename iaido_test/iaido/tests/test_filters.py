from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from ..models import Person
from ..filters import PersonFilter


class FilterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        person1 = Person.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@mail.com',
            date_of_birth=date(1990, 1, 1),
            age=33,
            username='johndoe'
        )
        person2 = Person.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='janesmith@mail.com',
            date_of_birth=date(1995, 6, 15),
            age=28, username='janesmith'
        )
        person3 = Person.objects.create(
            first_name='John',
            last_name='Johnson',
            email='johnjohnson@mail.com',
            date_of_birth=date(1985, 3, 10),
            age=38,
            username='johnjohnson'
        )

    def test_filter_by_first_name(self):
        response = self.client.get('/api/persons/filtered_persons/', {'first_name': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['first_name'], 'John')
        self.assertEqual(response.data[1]['first_name'], 'John')

    def test_filter_by_age(self):
        filter_params = {'min_age': 25, 'max_age': 29}
        response = self.client.get('/api/persons/filtered_persons/', filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Jane')
        self.assertEqual(response.data[0]['last_name'], 'Smith')

    def test_filter_by_multiple_fields(self):
        filter_params = {'first_name': 'John', 'min_age': 25, 'max_age': 35}
        response = self.client.get('/api/persons/filtered_persons/', filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')
        self.assertEqual(response.data[0]['last_name'], 'Doe')
