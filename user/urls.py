from django.urls import path
from .views import *

urlpatterns = [
    path('register', reg),
    path('login', login),
    path('logout', logout),
    path('login_info', login_info),
    path('avatar', avatar),
    path('user_ratings', user_ratings),
    path('recommend', recommend)
]