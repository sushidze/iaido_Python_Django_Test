from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Person


class PersonSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            hashed_password = make_password(password)
            validated_data['password'] = hashed_password
        return super().update(instance, validated_data)

    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'age', 'username', 'password']


class FilteredPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'age']
