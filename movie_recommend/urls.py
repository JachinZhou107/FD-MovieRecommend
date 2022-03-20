from django.urls import path
from .views import *

urlpatterns = [
    path('add_movie',add_movie),
    path('show_movies',show_movies),
]