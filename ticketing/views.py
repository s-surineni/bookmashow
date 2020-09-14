from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Auditorium, Movie, Multiplex
from .permissions import IsOwnerOrReadOnly
from .serializers import AuditoriumSerializer, MovieSerializer, UserSerializer
from ticketing import models
from ticketing import serializers


class UserViewSet(viewsets.ModelViewSet):
    '''API endpoint that allows users to be viewed or edited'''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class AuditoriumViewSet(viewsets.ModelViewSet):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer


class MultiplexViewSet(viewsets.ModelViewSet):
    queryset = Multiplex.objects.all()
    serializer_class = serializers.MultiplexSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = models.Seat.objects.all()
    serializer_class = serializers.SeatSerializer


class ScreeningViewSet(viewsets.ModelViewSet):
    queryset = models.Screening.objects.all()
    serializer_class = serializers.ScreeningSerializer

    @action(detail=True)
    def seats(self, request, *args, **kwargs):
        screening_obj = self.get_object()
        auditorium_obj = screening_obj.auditorium
        auditorium_seats = auditorium_obj.seats.all()
        all_reservations = models.Reservation.objects.filter(screening=screening_obj)
        all_reserved_seats = []
        for a_res in all_reservations:
            all_reserved_seats += list(a_res.seats.objects.all())
        seat_resp = []
        for a_seat in auditorium_seats:
            reserved = a_seat in all_reserved_seats
            seat_resp.append((a_seat.row, a_seat.number, reserved))

        return Response(seat_resp)
