from django.views.decorators.csrf import csrf_exempt
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'movie', views.MovieViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'auditorium', views.AuditoriumViewSet)
router.register(r'multiplex', views.MultiplexViewSet)
router.register(r'seat', views.SeatViewSet)
router.register(r'screening', views.ScreeningViewSet)
# router.register(r'reservation', views.Reservation)

urlpatterns = [
    path('', include(router.urls)),
    path('reservation/', csrf_exempt(views.Reservation.as_view()),
         name='reservation')
]
