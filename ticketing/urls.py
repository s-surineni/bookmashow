from django.urls import include, path
from rest_framework import routers

from . import views


urlpatterns = [
    path('movies/', views.MovieList.as_view()),
]
