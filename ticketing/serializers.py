from django.contrib.auth.models import User
from rest_framework import serializers

from ticketing import models
from ticketing.models import Auditorium, Movie, Multiplex, Screening


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration_minutes']


class ScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screening
        fields = ['movie', 'auditorium', 'screening_start']


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = ['name', 'multiplex']


class MultiplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multiplex
        fields = ['name']


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seat
        fields = ['row', 'number', 'auditorium']
