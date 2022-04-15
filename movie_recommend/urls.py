from django.urls import path
from .views import *

urlpatterns = [
    path('add_movie',add_movie),
    path('show_movies',show_movies),
    path('get_movie', get_movie),
    path('search_movie', search_movie),
    path('get_user_rating', get_user_rating),
    path('get_movie_ratings', get_movie_ratings),
    path('rating_movie', rating_movie),
    path('deal_movies', deal_movies)
]