from datetime import datetime
import json

# Create your views here.
import hashlib
import os

from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST, require_GET

from MovieRecommend import settings
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
    avatar = request.FILES.get('file')
    avatar_name = datetime.now().strftime('%Y%m%d%H%M%S%f') + avatar.name
    f = open(os.path.join(settings.UPLOAD_FILE, avatar_name), 'wb')
    for i in avatar.chunks():
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
