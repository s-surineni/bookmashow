from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''API endpoint that allows users to be viewed or edited'''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
