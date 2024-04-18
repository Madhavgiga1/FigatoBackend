"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

"""generics.CreateAPIView is a class-based view provided by Django REST 
Framework for handling HTTP POST requests to create new objects.

It inherits from generics.GenericAPIView, which provides 
the basic functionality for processing requests and responses.

CreateAPIView adds behavior specific to creating objects by 
using a serializer class specified in the serializer_class attribute.
"""
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


"""ObtainAuthToken is a class-based view provided by Django REST Framework
 for obtaining authentication tokens.

It handles HTTP POST requests with user credentials (such as email and 
password) to authenticate users and generate authentication tokens.

It inherits from APIView, the base class for all class-based views in Django REST Framework."""
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user