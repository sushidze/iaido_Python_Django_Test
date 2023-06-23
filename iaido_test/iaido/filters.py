from datetime import date

import django_filters

from .models import Person


class PersonFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    min_age = django_filters.NumberFilter(field_name='date_of_birth', method='filter_by_min_age', label='min_age')
    max_age = django_filters.NumberFilter(field_name='date_of_birth', method='filter_by_max_age', label='max_age')

    def filter_by_min_age(self, queryset, name, value):
        today = date.today()
        min_birthdate = today.replace(year=today.year - int(value))
        return queryset.filter(date_of_birth__lte=min_birthdate)

    def filter_by_max_age(self, queryset, name, value):
        today = date.today()
        max_birthdate = today.replace(year=today.year - int(value) - 1)
        return queryset.filter(date_of_birth__gte=max_birthdate)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'min_age', 'max_age']
