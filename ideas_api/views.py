from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route

from . import models
from . import serializers
from . import permissions

from datetime import datetime
from django.utils import timezone

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating users."""

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnUser,)
"""
    # For GET Requests
    @list_route(url_path='ideas')
    def get_ideas(self, request):
       #Return a list of ideas of the current logged in user.

        return Response({'status': 'GET'})

    # For POST Requests
    @detail_route(methods=['post'], url_path='idea')
    def update_idea(self, request, pk):
        #Updates the idea identified by the pk.
        serializer = serializers.IdeaSerializer(data=request.data)
        return Response(serializer)
"""

class LoginViewSet(viewsets.ViewSet):
    """Check email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class IdeaViewSet(viewsets.ModelViewSet):
    """Handles creating, reading, updating and deleting ideas."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.IdeaSerializer  
    permission_classes = (permissions.PostOwnIdea, IsAuthenticated)

    def get_queryset(self):
        id = self.kwargs['id']
        return models.Idea.objects.filter(user_id=id) 

    def perform_create(self, serializer):
        """Set the idea to the logged in user."""

        serializer.save(user_id=self.request.user)

    def perform_update(self, serializer):
        """Handles updating idea of the current user by changing the modification date."""

        serializer.save(modification_date=timezone.now())


        
        