import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from rest_framework import filters, generics, mixins, permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

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


class MovieListView(generics.ListAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class Reservation(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self, request, *args, **kwargs):
        post_data = json.loads(request.body)
        reservation_obj = models.Reservation()
        reservation_obj.screening = models.Screening.objects.get(
            pk=post_data['screening'])
        reservation_obj.save()
        # reservation_obj.user = request.user
        reservation_obj.user = User.objects.get(pk=(post_data['user']))
        for a_seat in post_data['seats']:
            models.SeatReserved.objects.create(
                seat=models.Seat.objects.get(pk=a_seat),
                reservation=reservation_obj,
                screening=models.Screening.objects.get(
                    pk=post_data['screening']))
        return Response({'success': True})



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
