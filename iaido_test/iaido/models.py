from django.db import models

from .exceptions import InvalidAgeException
from .utils import get_age


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    age = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)

    def clean(self):
        calculated_age = self.age
        expected_age = get_age(self.date_of_birth)
        if calculated_age != expected_age:
            raise InvalidAgeException()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
