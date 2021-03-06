# Create your views here.
import random
import re

import requests

from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import execjs

from user.models import User
from user.views import UserBasedCF
from .models import Movie, MovieRating, MovieLens

from datetime import date, datetime
from urllib.parse import urlencode
from lxml import html

etree = html.etree
# 伪装成浏览器
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
base_url = 'https://search.douban.com/movie/subject_search'
IP_AGENTS = [
    "http://58.240.53.196:8080",
    "http://219.135.99.185:8088",
    "http://117.127.0.198:8080",
    "http://58.240.53.194:8080"
]
# 设置IP代理

proxies = {"http": random.choice(IP_AGENTS)}


def spider_movie_info(movie_url):
    movies = {}
    res = requests.get(movie_url, headers={'User-agent': ua}, proxies=proxies)
    res = res.text
    html_tree = etree.HTML(res)

    title = html_tree.xpath("//div[@id='content']//h1/span/text()")

    movies['豆瓣链接'] = movie_url
    movies['电影标题'] = title[0].strip()
    movies['上映时间'] = title[1].strip().replace('(', '').replace(')', '')

    pic = html_tree.xpath("//div[@id='mainpic']/a/img/@src")
    movies['电影海报'] = re.sub(r'[ls]_ratio_poster', 'm_ratio_poster', pic[0])

    desc = html_tree.xpath("//div[@class='related-info']/div[@class='indent']/span[@class='all hidden']//text()")
    desc1 = html_tree.xpath("//div[@class='related-info']/div[@class='indent']/span[@property='v:summary']//text()")
    print(desc, desc1)
    if len(desc) > 0:
        movies['电影简介'] = "<br>".join(desc).strip()
    elif len(desc1) > 0:
        movies['电影简介'] = "<br>".join(desc1).strip()
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
        elif nsub_str.startswith('又名'):
            movies['电影别名'] = nsub_str.replace("又名:", "").strip()
        elif nsub_str.startswith('片长'):
            movies['电影片长'] = nsub_str.replace("片长:", "").strip()
        elif nsub_str.startswith('IMDb'):
            movies['imdbId'] = int(nsub_str.replace("IMDb: tt", "").strip())
    return movies


def spider_search_movie(movie_name, movie_year):
    d = {'search_text': movie_name}

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
            item_url = item.get('url', 'none')
            if item_url.count('/subject/') > 0:
                r = re.search(r'\(\d{4}\)$', item.get('title', 'none'))
                if r:
                    item_year = r.group(0)
                    item_year = int(item_year.replace('(', '').replace(')', ''))
                    if item_year == movie_year:
                        movie_url = item['url']
                        print(movie_year, item_year)
                        break
    print(movie_url)
    if movie_url == 'no result':
        return movie_url
    movies = spider_movie_info(movie_url)
    return movies
    # writer.writerow(movies)


def update_movie_info(movie, movie_info):
    if len(movie_info['电影标题'].encode('utf8')) > len(movie_info['电影标题']):
        s = movie_info['电影标题'].split(" ", 1)
        movie.movie_title = s[0]
        if len(s) > 1:
            movie.movie_name = s[1]
        else:
            movie.movie_name = ""
    else:
        movie.movie_title = ""
        movie.movie_name = movie_info['电影标题']
    movie.movie_other_name = movie_info.get('电影别名', '')
    movie.movie_time = movie_info.get('上映时间', '')
    movie.movie_score = movie_info.get('电影评分', '暂无')
    movie.movie_score_sum = movie_info.get('评分人数', '0人评价')
    movie.movie_actors = movie_info.get('电影主演', '')
    movie.movie_type = movie_info.get('电影类型', '')
    movie.movie_director = movie_info.get('电影导演', '')
    movie.movie_desc = movie_info.get('电影简介', '暂无简介')
    movie.movie_country = movie_info.get('电影产地', '')
    movie.movie_length = movie_info.get('电影片长', '')
    movie.movie_db_url = movie_info.get('豆瓣链接', 'none')
    movie.movie_imdb_id = movie_info.get('imdbId', 'none')
    movie.movie_poster = movie_info.get('电影海报', '')
    movie.movie_update_time = date.today().strftime('%Y-%m-%d')
    movie.save()
    return


def add_movie_info(movie_info):
    old_movies = Movie.objects.filter(movie_imdb_id=movie_info['imdbId'])
    if len(old_movies) > 0:
        movie = old_movies[0]
        if len(old_movies) > 1:
            for dou_movie in old_movies:
                if str(dou_movie.movie_imdb_id) != str(movie.movie_imdb_id):
                    dou_movie.delete()
    else:
        movie = Movie()
        movie.save()
    update_movie_info(movie, movie_info)
    return


@require_http_methods(['GET'])
def add_movie(request):
    response = {}
    movie = spider_search_movie(request.GET.get('movieName'), request.GET.get('movieTime'))
    if movie == 'no result':
        response['msg'] = '没有找到此电影'
        response['error'] = 1
        return JsonResponse(response)
    add_movie_info(movie)
    response['movie'] = movie
    response['msg'] = 'success'
    response['error'] = 0
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_movies(request):
    response = {}
    list_type = int(request.GET.get('listType') or 0)
    if list_type == 0:
        cats = ' 爱情 喜剧 动画 剧情 恐怖 惊悚 科幻 动作 悬疑 犯罪 冒险 战争 奇幻 运动 家庭 古装 武侠 西部 历史 传记 歌舞 黑色电影 纪录片 音乐 灾难 青春 儿童'.split(' ')
        years = ' 2022 2021 2020 2019 2018 2017 2016 2015 2014 2013 2012 2011 2000-2010 更早'.split(' ')
    else:
        catsEn = ' Action Adventure Animation Biography Comedy Crime Drama Family Fantasy History Horror Music Mystery ' \
               'Romance Sci-Fi Short Sport Thriller War Western Musical Film-Noir Documentary'.split(' ')
        catsZn = ' 动作 冒险 动画 传记 喜剧 犯罪 剧情 家庭 奇幻 历史 恐怖 音乐 悬疑 爱情 科幻 短片 运动 惊悚 战争 西部 歌舞片 黑色电影 纪录片'.split(' ')
        years = ' 2018 2017 2016 2015 2014 2013 2012 2011 2010 2009 2008 2007 2006 2005 2004 2003 2002 2001 2000 更早' \
            .split(' ')
    sources = ' 中国大陆 美国 韩国 日本 中国香港 中国台湾 泰国 印度 法国 英国 俄罗斯 意大利 西班牙 德国 波兰 澳大利亚'.split(' ')
    page = int(request.GET.get('page') or 1)
    page_size = int(request.GET.get('pageSize') or 12)
    cat_id = int(request.GET.get('catId') or 0)
    source_id = int(request.GET.get('sourceId') or 0)
    year_id = int(request.GET.get('yearId') or 0)
    try:
        # print(sources[source_id], years[year_id], catsEn[cat_id])
        if list_type == 0:
            movies = Movie.objects.filter(movie_country__contains=sources[source_id], movie_type__contains=cats[cat_id])
            if 0 < year_id <= 12:
                movies = movies.filter(movie_time=int(years[year_id]))
            elif year_id == 13:
                movies = movies.filter(movie_time__gte=2000, movie_time__lte=2010)
            elif year_id > 13:
                movies = movies.filter(movie_time__lt=2000)
        else:
            movies = MovieLens.objects.filter(Q(movie_type__icontains=catsEn[cat_id]) |
                                              Q(movie_type__contains=catsZn[cat_id])).order_by('-movie_time', 'id')
            if 19 >= year_id > 0:
                movies = movies.filter(movie_time=int(years[year_id]))
            elif year_id > 19:
                movies = movies.filter(movie_time__lt=2000)
        paged_movies = Paginator(movies, page_size)
        res_page = paged_movies.page(page).object_list
        total_pages = paged_movies.num_pages
        total_elements = paged_movies.count
        response['list'] = json.loads(serializers.serialize("json", res_page))
        if list_type == 1:
            for item in response['list']:
                item['pk'] = 'mr' + str(item['pk'])
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
        if str(movie_id).startswith('mr'):
            new_movie_id = str(movie_id).replace('mr', '')
            movie = MovieLens.objects.filter(id=new_movie_id)[0]
        else:
            movie = Movie.objects.filter(id=movie_id)[0]
        last_update_date = str(movie.movie_update_time)
        last_update_date = date.fromisoformat(last_update_date)
        today = date.today()
        print((today - last_update_date).days)
        if (today - last_update_date).days > 90:
            if str(movie.movie_db_url) == 'none':
                new_movie_info = spider_search_movie(movie.movie_name, movie.movie_time)
                if new_movie_info == 'no result':
                    new_movie_info = spider_search_movie(movie.movie_title, movie.movie_time)
            else:
                new_movie_info = spider_movie_info(str(movie.movie_db_url))
            print(new_movie_info)
            if new_movie_info == 'no result':
                raise Exception('电影信息错误或失效，可向本站管理员反馈')
            update_movie_info(movie, new_movie_info)

        if str(movie_id).startswith('mr'):
            new_movie_id = str(movie_id).replace('mr', '')
            res_movie = json.loads(serializers.serialize("json", MovieLens.objects.filter(id=new_movie_id)))[0]
        else:
            res_movie = json.loads(serializers.serialize("json", Movie.objects.filter(id=movie_id)))[0]
        response['movie'] = res_movie
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def search_movie(request):
    response = {}
    page = int(request.GET.get('page') or 1)
    # page_size = int(request.GET.get('pageSize') or 12)
    movie_name = request.GET.get('movieName')
    movie_set_num = int(request.GET.get('movieSet'))
    print(movie_set_num == 1)
    total_elements = 0
    response['keyWords'] = movie_name
    try:
        if movie_set_num == 0:
            movie_set = Movie
        else:
            movie_set = MovieLens
        movies = movie_set.objects.filter(
            Q(movie_name__icontains=movie_name) | Q(movie_title__icontains=movie_name) | Q(
                movie_other_name__icontains=movie_name)).order_by('-movie_time', 'id')
        paged_movies = Paginator(movies, 12)
        total_pages = paged_movies.num_pages
        total_elements = paged_movies.count
        res_page = paged_movies.page(page).object_list
        response['list'] = json.loads(serializers.serialize("json", res_page))
        if movie_set_num == 1:
            for item in response['list']:
                print(item)
                item['pk'] = 'mr' + str(item['pk'])
        response['totalPages'] = total_pages
        response['totalElements'] = total_elements
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['totalElements'] = total_elements
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)


@require_http_methods(['POST'])
def get_movie_ratings(request):
    response = {}
    data = json.loads(request.body)
    movie_imdb_id = data['movieImdbId']
    try:
        rating_items = MovieRating.objects.filter(movie_imdb_id=movie_imdb_id).order_by('-time_stamp')
        rating_list = json.loads(serializers.serialize("json", rating_items))
        for item in rating_list:
            user_id = int(item['fields']['user_id']) - 1000
            user = User.objects.filter(id=user_id)
            if len(user) > 0:
                item['fields']['user_avatar'] = str(user[0].avatar_url)
                item['fields']['username'] = str(user[0].username)
            else:
                item['fields']['user_avatar'] = '/static/user_avatar.jpg'
                item['fields']['username'] = '用户' + str(item['fields']['user_id'])
        response['list'] = rating_list
        print(response['list'])
        response['msg'] = 'success'
        response['error'] = 0
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def deal_movies(request):
    response = {
        'error': '0'
    }
    movie_lens = Movie.objects.filter()
    for movie in movie_lens:
        if str(movie.movie_imdb_id) != 'none':
            movie.movie_imdb_id = str(int(movie.movie_imdb_id))
        movie.save()
    return JsonResponse(response)
