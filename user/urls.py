from django.urls import path
from .views import *

urlpatterns = [
    path('register', reg),
    path('login', login),
    path('logout', logout),
    path('login_info', login_info),
    path('avatar', avatar),
    path('rating_movie', rating_movie),
    path('user_ratings', user_ratings),
    path('get_user_rating', get_user_rating),
    path('delete_rating', delete_user_rating),
    path('recommend', recommend)
]