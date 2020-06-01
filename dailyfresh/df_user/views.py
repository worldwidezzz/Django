from django.shortcuts import render, redirect, HttpResponseRedirect
from df_user.models import *
from hashlib import sha1
from django.http import HttpResponse, JsonResponse
from .islogin import islogin


def register(request):
    return render(request, 'df_user/register.html')


# 登录处理
def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf8"))
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功，转向登录界面
    return redirect('/user/login/')


# 判断用户是否存在
def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uanme=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 根据用户名查询对象
    user = UserInfo.objects.filter(uname=uname)  # []
    print(uname)
    # 判断：如果未查询到用户名错误
    if len(user) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == user[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


# 登录用户中心
@islogin
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail

    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id_list = goods_ids.split(',')
    good_list = []
    if len(goods_ids):
        for goods_id in goods_id_list:
            good_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {
        'titel': '用户中心',
        'user_email': user_email,
        'user_name': request.session['user_name'],
        'page_name': 1, 'info': 1,
        'goods_list': goods_list,
    }
    return render(request, 'df_user/user_center_info.html', context)


@islogin
def order(request):
    context = {'title': '用户中心', 'page_name': 1, 'order': 1}
    return render(request, 'df_user/user_center_order.html', context)


@islogin
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.uyoubian = post.get('uyoubian')
        user.save()
    context = {'title': '用户中心', 'user': user, 'page_name': 1, 'site': 1}
    return render(request, 'df_user/user_center_site.html', context)

