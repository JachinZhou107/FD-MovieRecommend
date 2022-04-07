# Create your views here.
import random
import re
import requests

from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import execjs

from .models import Movie

from urllib.parse import urlencode
from lxml import html

etree = html.etree
# 伪装成浏览器
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
base_url = 'https://search.douban.com/movie/subject_search'


def spider_movie_info(movie_name):
    IP_AGENTS = [

        "http://58.240.53.196:8080",

        "http://219.135.99.185:8088",

        "http://117.127.0.198:8080",

        "http://58.240.53.194:8080"

    ]

    # 设置IP代理

    proxies = {"http": random.choice(IP_AGENTS)}

    d = {'search_text': movie_name}

    movies = {}
    movie_url = 'no result'

    # req = Request('{}?{}'.format(base_url, urlencode(d)), headers={'User-agent': ua})
    # with urlopen(req, context=context, proxies=proxies) as res:
    res = requests.get('{}?{}'.format(base_url, urlencode(d)), headers={'User-agent': ua}, proxies=proxies)
    res = res.text
    r = re.search('window.__DATA__ = "([^"]+)"', res).group(1)
    with open('static/decode.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
        ctx = execjs.compile(decrypt_js)
        data = ctx.call('decrypt', r)
        for item in data['payload']['items']:
            print(item)
            if item.get('url', 'none').count('subject') > 0:
                movie_url = item['url']
                break
    print(movie_url)
    if movie_url == 'no result':
        return movie_url
    # req = Request(movie_url, headers={'User-agent': ua})
    # with urlopen(req, context=context) as res:
    #   res = res.read().decode('utf-8')
    res = requests.get(movie_url, headers={'User-agent': ua}, proxies=proxies)
    res = res.text
    html_tree = etree.HTML(res)

    title = html_tree.xpath("//div[@id='content']//h1/span/text()")
    movies['电影名'] = title[0].strip().split(" ", 1)[0]
    movies['电影原名'] = title[0].strip().split(" ", 1)[1]
    movies['上映时间'] = title[1].strip().replace('(', '').replace(')', '')

    pic = html_tree.xpath("//div[@id='mainpic']/a/img/@src")
    movies['电影海报'] = pic[0].replace('s_ratio_poster', 'm_ratio_poster')

    desc = html_tree.xpath("//div[@class='related-info']/div[@class='indent']/span//text()")
    movies['电影简介'] = desc[0].strip()

    score = html_tree.xpath("//div[contains(@class, 'rating_self')]/strong[contains(@class, 'rating_num')]/text()")
    score_sum = html_tree.xpath("//div[contains(@class, 'rating_self')]//div[contains(@class, 'rating_sum')]//text()")
    if len(score) > 0:
        movies['电影评分'] = score[0]
    else:
        movies['电影评分'] = '0'
    movies['评分人数'] = str.join('', score_sum).strip()

    info = html_tree.xpath("//div[@id='content']//div[@id='info']//text()")
    info_str = str.join('', info).strip()
    for sub_str in info_str.splitlines():
        nsub_str = sub_str.strip()
        if nsub_str.startswith('导演'):
            movies['电影导演'] = nsub_str.replace("导演:", "").strip()
        elif nsub_str.startswith('主演'):
            movies['电影主演'] = nsub_str.replace("主演:", "").strip()
        elif nsub_str.startswith('制片国家/地区'):
            movies['电影产地'] = nsub_str.replace("制片国家/地区:", "").strip()
        elif nsub_str.startswith('类型'):
            movies['电影类型'] = nsub_str.replace("类型:", "").strip()
        # elif nsub_str.startswith('上映日期'):
        #   movies['上映时间'] = nsub_str.replace("上映日期:","").strip()
        elif nsub_str.startswith('片长'):
            movies['电影片长'] = nsub_str.replace("片长:", "").strip()
        elif nsub_str.startswith('IMDb'):
            movies['imdbid'] = nsub_str.replace("IMDb: tt", "").strip()
    print(movies)
    return movies
    # writer.writerow(movies)


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
        movies = Movie.objects.filter(movie_contry__contains=sources[source_id], movie_type__contains=cats[cat_id],
                                      movie_time__contains=years[year_id])
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
        response['movies'] = json.loads(serializers.serialize("json", movies_by_name | movies_by_title))
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def deal_movie(request):
    response = {}
    movies = Movie.objects.filter()
    for movie in movies:
        # movie=movies[0]
        movie.movie_title = re.sub(r'》.*', "》", movie.movie_title)
        movie.save()
    response['msg'] = 'success'
    response['error'] = 0
    return JsonResponse(response)


@require_http_methods(['GET'])
def spider_movie(request):
    response = {}
    movie = spider_movie_info(request.GET.get('movieName'))
    if movie == 'no_result':
        response['msg'] = movie
        response['error'] = 1
        return JsonResponse(response)
    response['movie_info'] = movie
    response['msg'] = 'success'
    response['error'] = 0
    return JsonResponse(response)
