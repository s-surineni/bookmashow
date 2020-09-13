from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Movie
from .permissions import IsOwnerOrReadOnly
from .serializers import MovieSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''API endpoint that allows users to be viewed or edited'''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
