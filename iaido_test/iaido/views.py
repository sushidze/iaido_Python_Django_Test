from django.contrib.auth import authenticate
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import PersonFilter
from .models import Person
from .serialazers import FilteredPersonSerializer, PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Person objects.
    """
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
        """
        Custom action to retrieve filtered persons.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    API view for user login.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
