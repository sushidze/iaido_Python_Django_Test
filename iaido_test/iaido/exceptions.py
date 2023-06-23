from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidAgeException(APIException):
    """
    Exception raised for invalid age.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid age. Check date of birth or age.'
    default_code = 'invalid_age'
