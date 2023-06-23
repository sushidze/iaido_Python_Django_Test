from datetime import date

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler to return customized error responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'status': response.status_code,
            'message': response.data.get('detail', 'An error occurred.'),
        }
        response.data = custom_data

    return response


def get_age(date_of_birth):
    """
    Function for calculating age from date.
    """
    if date_of_birth is not None:
        today = date.today()
        years_difference = today.year - date_of_birth.year
        is_before_birthday = (
            today.month < date_of_birth.month or
            (today.month == date_of_birth.month and today.day < date_of_birth.day)
        )
        return years_difference - int(is_before_birthday)
    return None

