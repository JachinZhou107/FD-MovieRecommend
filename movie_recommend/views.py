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

from datetime import date
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
    res = requests.get(movie_url, headers={'User-agent': ua})
    res = res.text
    html_tree = etree.HTML(res)

    title = html_tree.xpath("//div[@id='content']//h1/span/text()")

    movies['豆瓣链接'] = movie_url
    movies['电影标题'] = title[0].strip()
    movies['上映时间'] = title[1].strip().replace('(', '').replace(')', '')

    pic = html_tree.xpath("//div[@id='mainpic']/a/img/@src")
    movies['电影海报'] = re.sub(r'[ls]_ratio_poster', 'm_ratio_poster', pic[0])

    desc = html_tree.xpath("//div[@class='related-info']/div[@class='indent']/span//text()")
    if len(desc) > 0:
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
            movies['imdbId'] = nsub_str.replace("IMDb: tt", "").strip()
    print(movies)
    return movies


def spider_search_movie(movie_name, movie_year):
    d = {'search_text': movie_name}

    movie_url = 'no result'

    # req = Request('{}?{}'.format(base_url, urlencode(d)), headers={'User-agent': ua})
    # with urlopen(req, context=context, proxies=proxies) as res:
    res = requests.get('{}?{}'.format(base_url, urlencode(d)), headers={'User-agent': ua})
    res = res.text
    r = re.search('window.__DATA__ = "([^"]+)"', res).group(1)
    with open('static/decode.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
        ctx = execjs.compile(decrypt_js)
        data = ctx.call('decrypt', r)
        for item in data['payload']['items']:
            # print(item)
            item_url = item.get('url', 'none')
            if item_url.count('/subject/') > 0:
                r = re.search(r'\(\d{4}\)$', item.get('title', 'none'))
                if r:
                    item_year = r.group(0)
                    item_year = item_year.replace('(', '').replace(')', '')
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
            movie.movie_name = s[0]
    else:
        movie.movie_title = ""
        movie.movie_name = movie_info['电影标题']
    movie.movie_time = movie_info.get('上映时间', '暂无')
    movie.movie_score = movie_info['电影评分'] or '暂无'
    movie.movie_score_sum = movie_info['评分人数']
    movie.movie_actors = movie_info.get('电影主演', '暂无')
    movie.movie_type = movie_info['电影类型'] or '暂无'
    movie.movie_director = movie_info.get('电影导演', '暂无')
    movie.movie_desc = movie_info['电影简介'] or '暂无'
    movie.movie_contry = movie_info['电影产地'] or '暂无'
    movie.movie_length = movie_info['电影片长'] or '暂无'
    movie.movie_db_url = movie_info['豆瓣链接'] or '暂无'
    movie.movie_imdb_id = movie_info['imdbId'] or '暂无'
    movie.movie_poster = movie_info['电影海报'] or '暂无'
    movie.movie_update_time = date.today().strftime('%Y-%m-%d')
    movie.save()
    return


def add_movie_info(movie_info):
    old_movies = Movie.objects.filter(movie_imdb_id=movie_info['imdbId'])
    if len(old_movies) > 0:
        movie = old_movies[0]
        if len(old_movies) > 1:
            for i in range(1, len(old_movies)):
                old_movies[i].delete()
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
    response['movie_info'] = movie
    response['msg'] = 'success'
    response['error'] = 0
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
        movie = Movie.objects.filter(id=movie_id)[0]
        last_update_date = str(movie.movie_update_time)
        last_update_date = date.fromisoformat(last_update_date)
        today = date.today()
        print((today - last_update_date).days)
        if (today - last_update_date).days > 180:
            new_movie_info = spider_search_movie(movie.movie_name, movie.movie_time)
            print(new_movie_info)
            update_movie_info(movie, new_movie_info)
        response['movie'] = json.loads(serializers.serialize("json", Movie.objects.filter(id=movie_id)))[0]
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
    total_elements = 0
    try:
        movies_by_name = Movie.objects.filter(movie_name__icontains=movie_name)
        movies_by_title = Movie.objects.filter(movie_title__icontains=movie_name)
        print(len(movies_by_name), len(movies_by_title))
        paged_movies = Paginator(movies_by_name | movies_by_title, 12)
        total_pages = paged_movies.num_pages
        total_elements = paged_movies.count
        res_page = paged_movies.page(page).object_list
        response['list'] = json.loads(serializers.serialize("json", res_page))
        response['totalPages'] = total_pages
        response['totalElements'] = total_elements
        response['msg'] = 'success'
        response['error'] = 0
    except Exception as e:
        response['totalElements'] = total_elements
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
