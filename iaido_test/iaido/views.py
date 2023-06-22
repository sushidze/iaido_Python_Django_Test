from django.contrib.auth import authenticate, login
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Person
from .filters import PersonFilter
from .serialazers import PersonSerializer, FilteredPersonSerializer, TokenSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    permission_classes = [permissions.IsAdminUser]
    pagination_class = PageNumberPagination
    filterset_class = PersonFilter

    def get_serializer_class(self):
        if self.action == 'filtered_persons':
            return FilteredPersonSerializer
        return PersonSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def filtered_persons(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
