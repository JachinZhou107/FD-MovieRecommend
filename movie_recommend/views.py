# Create your views here.
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from .models import Movie


@require_http_methods(["GET"])
def add_movie(request):
    response = {}
    try:
        movie = Movie(movie_name=request.GET.get('movie_name'), movie_time=request.GET.get('movie_time'))
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
    cats = ' 爱情 喜剧 动画 剧情 恐怖 惊悚 科幻 动作 悬疑 犯罪 冒险 战争 奇幻 运动 家庭 古装 武侠 西部 历史 传记 歌舞 黑色电影 纪录片 音乐 灾难 青春 儿童'.split(' ')
    years = ' 2022 2021 2020 2019 2018 2017 2016 2015 2014 2013 2012 2011 2000-2010 更早'.split(' ')
    sources = ' 中国大陆 美国 韩国 日本 中国香港 中国台湾 泰国 印度 法国 英国 俄罗斯 意大利 西班牙 德国 波兰 澳大利亚'.split(' ')
    page = int(request.GET.get('page') or 1)
    page_size = int(request.GET.get('pageSize') or 12)
    cat_id = int(request.GET.get('catId') or 0)
    source_id = int(request.GET.get('sourceId') or 0)
    year_id = int(request.GET.get('yearId') or 0)
    try:
        print(sources[source_id], years[year_id], cats[cat_id])
        movies = Movie.objects.filter(movie_contry__contains=sources[source_id], movie_type__contains=cats[cat_id], movie_time__contains=years[year_id])
        paged_movies = Paginator(movies, page_size)
        res_page = paged_movies.page(page).object_list
        total_pages = paged_movies.num_pages
        total_elements = paged_movies.count
        response['list'] = json.loads(serializers.serialize("json", res_page))
        response['totalPages'] = total_pages
        response['totalElements'] = total_elements
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def get_movie(request):
    response = {}
    movie_id = request.GET.get('movieId')
    try:
        movie = Movie.objects.filter(id=movie_id)
        response['movie'] = json.loads(serializers.serialize("json", movie))[0]
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)

@require_http_methods(['GET'])
def search_movie(request):
    response = {}
    movie_name = request.GET.get('movieName')
    try:
        movies_by_name = Movie.objects.filter(movie_name__icontains=movie_name)
        movies_by_title = Movie.objects.filter(movie_title__icontains=movie_name)
        print(movies_by_name, movies_by_title)
        response['movies'] = json.loads(serializers.serialize("json", movies_by_name|movies_by_title))
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)