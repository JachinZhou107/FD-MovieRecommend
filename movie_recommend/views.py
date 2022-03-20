from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from .models import Movie

@require_http_methods(["GET"])
def add_movie(request):
    response = {}
    try:
        movie = Movie(movie_name=request.GET.get('movie_name'))
        movie.save()
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)

@require_http_methods(['GET'])
def show_movies(request):
    response = {}
    try:
        movies = Movie.objects.filter()
        print(serializers.serialize("json",movies))
        response['list'] = json.loads(serializers.serialize("json",movies))
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)