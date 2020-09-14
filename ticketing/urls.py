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

urlpatterns = [
    path('', include(router.urls)),
]
