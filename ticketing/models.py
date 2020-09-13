from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration_minutes = models.IntegerField()
    auditorium = models.ForeignKey('Auditorium', on_delete=models.CASCADE)


class Auditorium(models.Model):
    name = models.CharField(max_length=100)
    multiplex = models.ForeignKey('Multiplex', on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}'.format(self.multiplex.name,
                               self.name)


class Screening(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    auditorium = models.ForeignKey('Auditorium', on_delete=models.CASCADE)
    screening_start = models.DateTimeField()


class Seat(models.Model):
    row = models.CharField(max_length=50)
    number = models.IntegerField()
    auditorium = models.ForeignKey('Auditorium', on_delete=models.CASCADE)


class Reservation(models.Model):
    screening = models.ForeignKey('Screening', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class SeatReserved(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)


class Multiplex(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
