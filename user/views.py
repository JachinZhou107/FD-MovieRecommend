import math
from datetime import datetime
import json

# Create your views here.
import hashlib
import os

from django.core import serializers
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST, require_GET

from MovieRecommend import settings
from movie_recommend.models import MovieRating, Movie, MovieLens
from user.models import User


@require_POST
def reg(request):
    # 用户注册逻辑代码
    response = {}
    # 处理提交数据
    data = json.loads(request.body)
    print(data)
    username = data['username']
    if not username:
        response['msg'] = '请输入正确的用户名'
        response['error'] = 1
        return JsonResponse(response)
    password_1 = data['password_1']
    # 1 生成hash算法对象对密码进行加密
    m = hashlib.md5()
    # 2 对待加密明文使用update方法！要求输入明文为字节串
    m.update(password_1.encode())
    # 3 调用对象的 hexdigest[16进制],通常存16进制
    password_m1 = m.hexdigest()
    print(password_m1)  # 加密后的密文会显示在终端上
    password_2 = data['password_2']
    # 对password_2执行MD5加密处理
    m = hashlib.md5()
    m.update(password_2.encode())
    password_m2 = m.hexdigest()
    print(password_m2)
    # 可以设定密码格式，判断是都符合
    if not password_m1 or not password_m2:
        response['msg'] = '请输入正确的密码'
        response['error'] = 1
        return JsonResponse(response)
    # 判断两次密码输入是否一致
    if password_m1 != password_m2:
        response['msg'] = '两次密码不一致'
        response['error'] = 1
        return JsonResponse(response)
    # 查询用户名是否已注册过
    try:
        old_user = User.objects.get(username=username)
        # 当前用户名已被注册
        response['msg'] = '用户名已经被注册'
        response['error'] = 1
        return JsonResponse(response)
    except Exception as e:
        # 若没查到的情况下进行报错，则证明当前用户名可用
        print('%s是可用用户名--%s' % (username, e))
        try:
            user = User.objects.create(username=username, password=password_m1)
            # 注册成功后
            response['username'] = username
            response['avatar'] = user.avatar_url
            response['msg'] = '注册成功'
            response['error'] = 0
            # 存session
            request.session['username'] = username
            return JsonResponse(response)
        # 若创建不成功会抛出异常
        except Exception as e:
            # 还可能存在用户名被重复使用的情况
            print(e)
            response['msg'] = '用户名已经被注册'
            response['error'] = 1
            return JsonResponse(response)


@require_POST
# 用户的登录逻辑处理
def login(request):
    response = {}
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    m = hashlib.md5()
    m.update(password.encode())
    password_m = m.hexdigest()
    # 判断输入是否其中一项为空或者格式不正确
    if not username or not password:
        response['msg'] = '用户名或者密码格式错误 !'
        response['error'] = 1
        return JsonResponse(response)
    # 若输入没有问题则进入数据比对阶段，看看已经注册的用户中是否存在该用户
    users = User.objects.filter(username=username, password=password_m)
    # 由于使用了filter, 所以返回值user是一个数组，但是也要考虑其为空的状态，即没有查到该用户
    if not users:
        response['msg'] = '用户不存在或用户密码输入错误!!'
        response['error'] = 1
        return JsonResponse(response)
    # 返回值是个数组，并且用户名具备唯一索引，当前用户是该数组中第一个元素
    user = users[0]
    response['username'] = username
    response['avatar'] = user.avatar_url
    response['msg'] = '登录成功'
    response['error'] = 0
    request.session['username'] = username
    resp = JsonResponse(response)
    # 检查post 提交的所有键中是否存在 isSaved 键
    print(data['isStay'])
    if data['isStay']:
        # 若存在则说明用户选择了记住用户名功能，执行以下语句设置cookie的过期时间
        username = json.dumps(username)
        resp.set_cookie('username', username, 60 * 60 * 24 * 7)
    return resp


@require_GET
def logout(request):
    # 实现退出功能
    response = {}
    # 删除session
    if 'username' in request.session:
        del request.session['username']
    response['msg'] = '退出登录成功'
    response['error'] = 0
    resp = JsonResponse(response)
    # 删除cookie
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    return resp


@require_GET
def login_info(request):
    # 实现检查登录信息功能
    response = {}
    if 'username' in request.COOKIES:  # 检查cookie，是否保存了用户登录信息
        # 若存在则赋值回session
        username = json.loads(request.COOKIES['username'])
        request.session['username'] = username
    if 'username' in request.session:  # request.session 类字典对象
        user = User.objects.get(username=request.session['username'])
        response['avatar'] = user.avatar_url
        response['userId'] = user.id
        response['username'] = request.session['username']
        response['login'] = 1
        return JsonResponse(response)
    else:
        response['username'] = ''
        response['login'] = 0
        return JsonResponse(response)


@require_POST
def avatar(request):
    # 实现上传用户头像
    response = {}
    if 'username' not in request.session:
        response['msg'] = '请先登录'
        response['error'] = 1
        return JsonResponse(response)
    username = request.session['username']
    avatar_item = request.FILES.get('file')
    avatar_name = datetime.now().strftime('%Y%m%d%H%M%S%f') + avatar_item.name
    f = open(os.path.join(settings.UPLOAD_FILE, avatar_name), 'wb')
    for i in avatar_item.chunks():
        f.write(i)
    f.close()
    try:
        user = User.objects.get(username=username)
        user.avatar_url = 'http://127.0.0.1:8000/static/' + avatar_name
        user.save()
        response['msg'] = '修改头像成功'
        response['error'] = 0
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = '未找到用户信息'
        response['error'] = 1
        return JsonResponse(response)


@require_POST
def get_user_rating(request):
    response = {}
    data = json.loads(request.body)
    movie_imdb_id = data['movieImdbId']
    user_id = str(int(data['userId']) + 1000)
    try:
        rating_item = MovieRating.objects.get(movie_imdb_id=movie_imdb_id, user_id=user_id)
        response['rating'] = float(rating_item.rating)
        response['comments'] = str(rating_item.comments)
        response['time_stamp'] = str(rating_item.time_stamp)
        response['msg'] = 'success'
        response['error'] = 0
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)


@require_POST
def rating_movie(request):
    response = {}
    data = json.loads(request.body)
    movie_imdb_id = data['movieImdbId']
    rating = data['rating']
    comments = data['comments']
    time_stamp = int(datetime.now().timestamp())
    user_id = str(int(data['userId']) + 1000)
    try:
        movie_rating_set = MovieRating.objects.filter(user_id=user_id, movie_imdb_id=movie_imdb_id)
        if len(movie_rating_set) > 0:
            movie_rating = movie_rating_set[0]
        else:
            movie_rating = MovieRating()

        movie_rating.movie_imdb_id = movie_imdb_id
        movie_rating.user_id = user_id
        movie_rating.rating = rating
        movie_rating.comments = comments
        movie_rating.time_stamp = time_stamp
        update_sim(1, movie_rating)
        movie_rating.save()
        response['msg'] = 'success'
        response['error'] = 0
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error'] = 1
    return JsonResponse(response)


@require_GET
def user_ratings(request):
    response = {}
    user_id = request.GET.get('userId')
    user_id = str(int(user_id) + 1000)
    try:
        ratings_qs = MovieRating.objects.filter(user_id=user_id)
        ratings_list = json.loads(serializers.serialize("json", ratings_qs))
        for rating in ratings_list:
            movie = {}
            movie_qs = MovieLens.objects.filter(movie_imdb_id=rating['fields']['movie_imdb_id'])
            if len(movie_qs) < 1:
                movie_qs = Movie.objects.filter(movie_imdb_id=rating['fields']['movie_imdb_id'])
                movie['movieId'] = str(movie_qs[0].id)
            else:
                movie['movieId'] = 'mr' + str(movie_qs[0].id)
            movie['movieName'] = str(movie_qs[0].movie_name)
            movie['movieTitle'] = str(movie_qs[0].movie_title)
            movie['moviePoster'] = str(movie_qs[0].movie_poster)
            rating['movie'] = movie
        response['ratings'] = ratings_list
        response['error'] = 0
        response['msg'] = 'success'
    except Exception as e:
        response['error'] = 1
        response['msg'] = str(e)
    return JsonResponse(response)


@require_GET
def delete_user_rating(request):
    response = {}
    user_id = str(int(request.GET.get('userId')) + 1000)
    rating_id = request.GET.get('ratingId')
    # try:
    rating_qs = MovieRating.objects.get(id=rating_id)
    if str(rating_qs.user_id) == user_id:
        update_sim(0, rating_qs)
        rating_qs.delete()
        response['msg'] = '删除评论成功'
        response['error'] = 0
    else:
        response['msg'] = '删除评论失败'
        response['error'] = 1
    # except Exception as e:
    #     response['msg'] = '评论不存在'
    #     response['error'] = 1
    return JsonResponse(response)


def get_recommend(cf, user_id):
    movie_list = []
    top_n_movie = cf.recommend(user_id)
    for rmovie in top_n_movie:
        movie_qs = MovieLens.objects.filter(movie_imdb_id=rmovie[0])
        print(rmovie, len(movie_qs))
        if len(movie_qs) < 1:
            movie_qs = Movie.objects.filter(movie_imdb_id=rmovie[0])
            movie = json.loads(serializers.serialize("json", movie_qs))[0]
        else:
            movie = json.loads(serializers.serialize("json", movie_qs))[0]
            movie['pk'] = 'mr' + str(movie['pk'])
        movie_list.append(movie)
    return movie_list


@require_GET
def recommend(request):
    response = {}
    movie_list = []
    user_id = str(int(request.GET.get('userId')) + 1000)
    user_cf = UserBasedCF()
    item_cf = ItemBasedCF()
    try:
        response['moviesUserCF'] = get_recommend(user_cf, user_id)
        response['moviesItemCF'] = get_recommend(item_cf, user_id)
        response['error'] = 0
        response['msg'] = 'success'
    except Exception as e:
        response['error'] = 1
        response['msg'] = str(e)
    return JsonResponse(response)


# 用户-电影表
user2movie = dict()
# 物体-用户表
movie2users = dict()


def calc_user_sim():
    if len(movie2users) == 0 or len(user2movie) == 0:
        for rating_item in MovieRating.objects.filter():
            movie = str(rating_item.movie_imdb_id)
            user = str(rating_item.user_id)
            rating = str(rating_item.rating)
            user2movie.setdefault(user, {})
            user2movie[user][movie] = float(rating)
            if movie not in movie2users:
                movie2users[movie] = set()
            movie2users[movie].add(user)
    # 用户相似度字典
    UserBasedCF.user_sim_dct = dict()
    '''获取用户之间的相似度,存放在user_sim_dct中'''
    for movie, users in movie2users.items():
        for u in users:
            for v in users:
                if u == v:
                    continue
                UserBasedCF.user_sim_dct.setdefault(u, {})
                UserBasedCF.user_sim_dct[u].setdefault(v, 0)
                UserBasedCF.user_sim_dct[u][v] += 1 / math.log(1 + len(users))
    for u, users in UserBasedCF.user_sim_dct.items():
        for v, count in users.items():
            UserBasedCF.user_sim_dct[u][v] = count / math.sqrt(len(user2movie[u]) * len(user2movie[v]))

    # 按照key排序value，返回K个最相近的用户
    print("user similarity calculated!")
    # 格式是 [ (user, value), (user, value), ... ]
    return


def calc_movie_sim():
    if len(movie2users) == 0 or len(user2movie) == 0:
        for rating_item in MovieRating.objects.filter():
            movie = str(rating_item.movie_imdb_id)
            user = str(rating_item.user_id)
            rating = str(rating_item.rating)
            user2movie.setdefault(user, {})
            user2movie[user][movie] = float(rating)
            if movie not in movie2users:
                movie2users[movie] = set()
            movie2users[movie].add(user)
    # 物品相似度字典
    ItemBasedCF.movie_sim_dct = dict()
    '''获取物品之间的相似度,存放在movie_sim_dct中'''
    for user, movies in user2movie.items():
        for u in movies:
            for v in movies:
                if u == v:
                    continue
                ItemBasedCF.movie_sim_dct.setdefault(u, {})
                ItemBasedCF.movie_sim_dct[u].setdefault(v, 0)
                ItemBasedCF.movie_sim_dct[u][v] += 1 / math.log(1 + len(movies))
    for u, movies in ItemBasedCF.movie_sim_dct.items():
        for v, count in movies.items():
            ItemBasedCF.movie_sim_dct[u][v] = count / math.sqrt(len(movie2users[u]) * len(movie2users[v]))

    print("movie similarity calculated!")
    return


def update_sim(method, rating):
    movie_id = str(rating.movie_imdb_id)
    user_id = str(rating.user_id)

    UserBasedCF.user_sim_dct.pop(user_id, {})
    for movie, users in movie2users.items():
        if user_id in users:
            for u in users:
                if u == user_id:
                    continue
                UserBasedCF.user_sim_dct[u].pop(user_id, {})

    ItemBasedCF.movie_sim_dct.pop(movie_id, {})
    for user, movies in user2movie.items():
        if movies.get(movie_id, 'none') != 'none':
            for movie in movies:
                if movie == movie_id:
                    continue
                ItemBasedCF.movie_sim_dct[movie].pop(movie_id, {})

    if method == 1:
        user2movie.setdefault(user_id, {})
        user2movie[user_id][movie_id] = float(str(rating.rating))
        if movie_id not in movie2users:
            movie2users[movie_id] = set()
        movie2users[movie_id].add(user_id)
    elif method == 0:
        user2movie[user_id].pop(movie_id, {})
        movie2users[movie_id].remove(user_id)

    if len(movie2users[movie_id]) == 0:
        movie2users.pop(movie_id, {})

    if len(user2movie[user_id]) == 0:
        user2movie.pop(user_id, {})

    for movie, users in movie2users.items():
        if user_id in users:
            for u in users:
                if u == user_id:
                    continue
                # 新增评价时，之前相似度表中可能两个用户都没有字段
                UserBasedCF.user_sim_dct.setdefault(u, {})
                UserBasedCF.user_sim_dct[u].setdefault(user_id, 0)
                UserBasedCF.user_sim_dct.setdefault(user_id, {})
                UserBasedCF.user_sim_dct[user_id].setdefault(u, 0)
                UserBasedCF.user_sim_dct[u][user_id] += 1 / math.log(1 + len(users))
                UserBasedCF.user_sim_dct[user_id][u] = UserBasedCF.user_sim_dct[u][user_id]

    if user_id in UserBasedCF.user_sim_dct:
        for u, count in UserBasedCF.user_sim_dct[user_id].items():
            UserBasedCF.user_sim_dct[user_id][u] = count / math.sqrt(len(user2movie[u]) * len(user2movie[user_id]))
            UserBasedCF.user_sim_dct[u][user_id] = UserBasedCF.user_sim_dct[user_id][u]

    print("user similarity updated!")

    for user, movies in user2movie.items():
        if movies.get(movie_id, 'none') != 'none':
            for movie in movies:
                if movie == movie_id:
                    continue
                ItemBasedCF.movie_sim_dct.setdefault(movie, {})
                ItemBasedCF.movie_sim_dct[movie].setdefault(movie_id, 0)
                ItemBasedCF.movie_sim_dct.setdefault(movie_id, {})
                ItemBasedCF.movie_sim_dct[movie_id].setdefault(movie, 0)
                ItemBasedCF.movie_sim_dct[movie][movie_id] += 1 / math.log(1 + len(movies))
                ItemBasedCF.movie_sim_dct[movie_id][movie] = ItemBasedCF.movie_sim_dct[movie][movie_id]

    if movie_id in ItemBasedCF.movie_sim_dct:
        for movie, count in ItemBasedCF.movie_sim_dct[movie_id].items():
            ItemBasedCF.movie_sim_dct[movie_id][movie] = count / math.sqrt(
                len(movie2users[movie]) * len(movie2users[movie_id]))
            ItemBasedCF.movie_sim_dct[movie][movie_id] = ItemBasedCF.movie_sim_dct[movie_id][movie]

    print("movie similarity updated!")
    return


class UserBasedCF(object):
    # 用户相似度
    user_sim_dct = dict()

    def __init__(self):
        # 最相似的30个用户
        self.K = 30
        # 推荐出10部影片
        self.N = 10
        if len(UserBasedCF.user_sim_dct) == 0:
            calc_user_sim()

    def recommend(self, user_id):
        rank = dict()
        print('user2movie', user2movie.get(user_id, 'none'))
        if user2movie.get(user_id, 'none') == 'none':
            return rank
        k_sim_users = sorted(UserBasedCF.user_sim_dct[user_id].items(), key=lambda x: -x[1])[:self.K]
        for sim_user, factor in k_sim_users:
            for imdb_id in user2movie[sim_user]:
                if imdb_id in user2movie[user_id]:
                    continue
                rank.setdefault(imdb_id, 0)
                rank[imdb_id] += factor * user2movie[sim_user][imdb_id]
        rank_n = sorted(rank.items(), key=lambda x: -x[1])[:self.N]
        print('user2movie', rank_n)
        return rank_n


class ItemBasedCF(object):
    # 物品（影片）似度
    movie_sim_dct = dict()

    def __init__(self):
        # 最相似的30个影片
        self.K = 30
        # 推荐出10部影片
        self.N = 10
        if len(ItemBasedCF.movie_sim_dct) == 0:
            calc_movie_sim()

    def recommend(self, user_id):
        rank = dict()
        if user2movie.get(user_id, 'none') == 'none':
            return rank
        for movie, rating_num in user2movie[user_id].items():
            for sim_movie, factor in sorted(ItemBasedCF.movie_sim_dct[movie].items(), key=lambda x: -x[1])[:self.K]:
                if user2movie[user_id].get(sim_movie, 'none') != 'none':
                    continue
                rank.setdefault(sim_movie, 0)
                rank[sim_movie] += factor * rating_num
        rank_n = sorted(rank.items(), key=lambda x: -x[1])[:self.N]
        print(rank_n)
        return rank_n


calc_movie_sim()
calc_user_sim()

