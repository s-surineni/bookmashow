from django.contrib.auth.models import User
from rest_framework import serializers

from ticketing import models
from ticketing.models import Auditorium, Movie, Multiplex, Screening


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    screenings = serializers.HyperlinkedRelatedField(many=True,
                                                     view_name='screening-detail',
                                                     read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration_minutes',
                  'screenings']


class ScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screening
        fields = ['movie', 'auditorium', 'screening_start']


class AuditoriumSerializer(serializers.HyperlinkedModelSerializer):
    seats = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=models.Seat.objects.all())
    class Meta:
        model = Auditorium
        fields = ['name', 'multiplex', 'seats']


class MultiplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multiplex
        fields = ['name']


class ReservationSerializer(serializers.ModelSerializer):
    # TODO: Make sure if this is necessary, as this is already available in model
    screening = serializers.HyperlinkedRelatedField(queryset=models.Screening.objects.all(),
                                                    view_name='screening-detail')
    seats = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name='screening-detail')

    class Meta:
        model = models.Reservation
        fields = ['user', 'screening', 'reserved_seats']


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seat
        fields = ['row', 'number', 'auditorium']
