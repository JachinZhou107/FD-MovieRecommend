from django.urls import path
from .views import *

urlpatterns = [
    path('add_movie',add_movie),
    path('show_movies',show_movies),
    path('get_movie', get_movie),
    path('search_movie', search_movie),
    path('deal_movie', spider_movie),
]