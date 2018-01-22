from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating users."""

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    