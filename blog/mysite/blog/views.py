from io import BytesIO
import uuid
import re
import logging

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
# from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST, require_safe
from .utils import require_login
from django.conf import settings
from django.core.paginator import Paginator

# Create your views here.
from . import models
from . import utils
from . import cacheUtils

def index(request):
    """
    博客首页面
    :param request:获取请求的数据
    :return:request参数、待渲染的模板文件、具体数据
    """
    logger = logging.getLogger("django")
    logger.debug("首页运行。。。")
    articles = cacheUtils.get_all_article()

    # 分页
    # 从setting配置文件中获取指定的每页显示的条数
    pageSize = int(request.GET.get("pageSize", settings.PAGE_SIZE))
    # 当前页
    pageNow = int(request.GET.get("pageNow", 1))
    # 构建一个Paginator对象
    paginator = Paginator(articles, pageSize)
    page = paginator.page(pageNow)
    return render(request, 'blog/index.html', {"page": page, "pageSize": pageSize})


def log_user(request):
    """
    用户登录
    :param request: 请求头对象
    :return:
    """
    logger = logging.getLogger("django")
    logger.debug("用户登录。。。")
    # user = request.GET
    # return render(request, 'blog/log_user.html', {})
    if request.method == 'GET':
        request.session['Error'] = 0
        return render(request, 'blog/log_user.html', {'msg': '输入账号密码'})
    elif request.method == 'POST':
        username = request.POST['account']
        log_password = request.POST['log_password']
        try:
            password = utils.hmac_by_md5(log_password)
            user = models.User.objects.get(username=username, password=password)
            # 保存登陆用户的信息
            request.session['loginUser'] = user
            print(user)
            response = redirect(reverse("blog:login_success"))
            response.set_cookie("username", username)
            if request.session['Error'] >= 2:
                # 接收验证码
                code = request.POST['code']

                # 判断验证码是否正确
                mycode = request.session['code']
                if code.lower() != mycode.lower():

                    return render(request, 'blog/log_user.html', {"msg": "验证码错误！"})

                # 删除session中的验证码
                del request.session['code']
            return response
        except Exception as e:
            print(e)
            request.session['Error'] += 1
            return render(request, 'blog/log_user.html', {'msg': '登陆失败！请重试'})


def reg_user(request):
    """
    注册
    :param request: 请求头对象
    :return:
    """
    logger = logging.getLogger("django")
    logger.debug("用户注册。。。")
    if request.method == "POST":
        # 接受参数
        # print(request.POST['nickname'])
        try:
            username = request.POST['username'].strip()
            nickname = request.POST['nickname'].strip()
            password = request.POST['password'].strip()
            con_password = request.POST['con-password'].strip()
            age = request.POST['age'].strip()
            gender = request.POST['gender']
            header = request.FILES.get('header')
            print(gender)

            # 接收验证码
            code = request.POST['code']
            print(code)

            # 判断验证码是否正确
            mycode = request.session['code']

            # 删除session中的验证码
            del request.session['code']

            # 数据验证
            if len(username) < 1:
                return render(request, 'blog/reg_user.html', {"msg": "用户账号不能为空"})
            u = models.User.objects.filter(username=username)
            # print(u)
            if len(u) > 0:
                return render(request, 'blog/reg_user.html', {"msg": "账号已存在"})
            if len(nickname) < 1:
                return render(request, 'blog/reg_user.html', {"msg": "用户昵称不能为空"})
            if len(con_password) < 6:
                return render(request, 'blog/reg_user.html', {"msg": "密码不能小于六位"})
            if con_password != password:
                return render(request, 'blog/reg_user.html', {"msg": "两次密码不一致"})
            if code.lower() != mycode.lower():
                return render(request, 'blog/reg_user.html', {"msg": "验证码错误！"})
            try:
                # 加密
                password = utils.hmac_by_md5(password)
                # print(header)
                # 上传图片
                # header = request.FILES.get('header', None)
                # print(request.FILES)
                # print(header)
                # path = "static/images/headers/" + uuid.uuid4().hex[:-15] + header.name
                # with open(path, "wb") as f:
                #     for file in header.chunks():
                #         f.write(file)
                user = models.User(username=username, nickname=nickname, password=password, age=age, header=header)
                user.save()

                # return render(request, "blog/all_user.html", {"msg": "恭喜您，注册成功！！"})
                return redirect("/blog/log_user/")

            except Exception as e:
                print(e)
                return render(request, 'blog/reg_user.html', {"msg": "图片上传失败"})

        except Exception as e:
            print(e)
            return render(request, "blog/reg_user.html", {"msg": "注册失败！！"})

    elif request.method == "GET":
        return render(request, 'blog/reg_user.html', {"msg": "请填写以下数据"})


@require_login
def del_user(request, user_id):
    """
    删除用户
    :param request: 请求头对象
    :param user_id: 需要操作的用户id号
    :return: 打印页面，返回用户数据
    """
    logger = logging.getLogger("django")
    logger.debug("删除用户。。。")
    # u_id = request.GET['id']
    user = models.User.objects.get(pk=user_id)
    print(user)
    user.delete()
    # return HttpResponse('<h2>删除成功<a href="/blog/all_user/">返回</a></h2>')
    return redirect('/blog/all_user/')


@require_login
def all_user(request):
    """
    全部用户
    :param request: 请求头对象
    :return: 打印页面，返回用户数据
    """
    logger = logging.getLogger("django")
    logger.debug("查看全部用户。。。")
    users = models.User.objects.all()
    # content = ""
    # for u in users:
    #     # print(u.name)
    #     content += "<h3>" + u.username + "<a href='/blog/del_user/?id=" + str(u.id) + "'>删除</a>" + "<h3>"
    # return HttpResponse(content)
    return render(request, 'blog/all_user.html', {"users": users})


@require_login
def login_success(request):
    """
    全部用户
    :param request: 请求头对象
    :return: 打印页面，返回用户数据
    """

    logger = logging.getLogger("django")
    logger.debug("用户登陆成功。。。")
    articles = models.Article.objects.all()
    # 分页
    # 从setting配置文件中获取指定的每页显示的条数
    pageSize = int(request.GET.get("pageSize", settings.PAGE_SIZE))
    # 当前页
    pageNow = int(request.GET.get("pageNow", 1))
    # 构建一个Paginator对象
    paginator = Paginator(articles, pageSize)
    page = paginator.page(pageNow)
    # return render(request, 'blog/index.html', {"page": page, "pageSize": pageSize})
    return render(request, 'blog/login_success.html', {"page": page, "pageSize": pageSize})


@require_login
def show_user(request, user_id):
    """
    展示信息
    :param request: 请求头对象
    :param user_id: 需要操作的用户id号
    :return: 打印页面，返回用户数据
    """
    logger = logging.getLogger("django")
    logger.debug("展示用户信息。。。")
    user = models.User.objects.get(id=user_id)
    print(user)
    return render(request, 'blog/show_user.html', {'user': user})


@require_login
def change_info(request, user_id):
    """
    修改信息
    :param request: 请求头对象
    :param user_id: 需要操作的用户id号
    :return: 打印页面，返回用户数据
    """
    logger = logging.getLogger("django")
    logger.debug("改变资料。。。")
    if request.method == "GET":
        user = models.User.objects.filter(id=user_id).first()
        return render(request, "blog/change_info.html", {"user": user})
    # 修改信息
    else:
        nickname = request.POST['nickname']
        age = request.POST['age']

        # 获取到需要修改的用户
        user = models.User.objects.get(id=user_id)
        # 修改数据
        user.nickname = nickname
        user.age = age
        # 保存修改后的数据
        user.save()
        return redirect('/blog/show_user/'+str(user_id)+'/')


@require_login
def user_change_info(request):
    logger = logging.getLogger("django")
    logger.debug("用户修改个人资料。。。")
    user = request.session['loginUser']
    print(user.username)
    user = models.User.objects.get(username=user.username)
    if request.method == "GET":
        return render(request, 'blog/user_change_info.html', {})
    else:
        try:
            # 上传图片
            print("1231")
            nickname = request.POST['nickname']
            age = request.POST['age']
            header = request.FILES.get('header', None)
            user.nickname = nickname
            user.age = age
            print(request.FILES)
            print(header)
            user.header = header
            user.save()
            del request.session['loginUser']
            request.session['loginUser'] = user
            return redirect(reverse("blog:user_change_info"), {"msg": "资料修改成功"})
        except Exception as e:
            print(e)
            return render(request, 'blog/user_change_info.html', {"msg": "图片上传失败"})


@require_login
def out_user(request):
    """
    退出
    :param request:请求头对象
    :return:
    """
    logger = logging.getLogger("django")
    logger.debug("用户退出。。。")
    try:
        del request.session['loginUser']
    finally:
        return redirect('/blog/index/')


# 文章操作
@require_login
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    logger = logging.getLogger("django")
    logger.debug("添加文章。。。")
    if request.method == 'GET':
        return render(request, 'blog/add_article.html', {"msg": "编辑文章🙂"})
    else:
        title = request.POST['title']
        content = request.POST['content']
        author = request.session['loginUser']
        print(title, content)
        if len(title) <= 0:
            return render(request, 'blog/add_article.html', {"msg": "标题不能为空😫"})
        elif len(content) <= 0:
            return render(request, 'blog/add_article.html', {"msg": "内容不能为空😫"})
        article = models.Article(title=title, content=content, author=author)
        article.save()

        # 更新缓存
        cacheUtils.get_all_article(change=True)
        # return render(request, "blog/show_article.html", {'article': article})
        return JsonResponse({"msg": "文章添加成功", "success": True})


@require_login
def del_article(request, a_id):
    """
    删除文章
    :param request: 请求头对象
    :param a_id:
    :return:
    """
    logger = logging.getLogger("django")
    logger.debug("删除文章。。。")
    article = models.Article.objects.get(id=a_id)
    article.delete()
    return redirect(reverse("blog:self_all_article"))


@require_login
def update_article(request, a_id):
    """
    修改文章
    :param request: 请求头对象
    :param a_id:
    :return:
    """
    logger = logging.getLogger("django")
    logger.debug("修改文章。。。")
    article = models.Article.objects.get(pk=a_id)
    if request.method == "GET":
        return render(request, "blog/update_article.html", {'article': article})
    else:
        title = request.POST['title']
        content = request.POST['content']
        article.title = title
        article.content = content
        article.save()
        return redirect(reverse("blog:show_article", kwargs={"a_id": a_id}))


@require_login
def show_article(request, a_id):
    """
    展示单篇文章信息
    :param request:请求头对象
    :param a_id:
    :return:
    """
    logger = logging.getLogger("django")
    logger.debug("展示单篇文章。。。")
    article = models.Article.objects.get(pk=a_id)
    return render(request, "blog/show_article.html", {'article': article})


def only_show_article(request, a_id):
    """
    展示单篇文章信息
    :param request:请求头对象
    :param a_id:
    :return:
    """
    article = models.Article.objects.get(pk=a_id)
    return render(request, "blog/only_show_article.html", {'article': article})


@require_login
def self_all_article(request):
    """
    展示登陆用户的所有文章
    :param request: 请求头对象
    :return:
    """
    logger = logging.getLogger("django")
    logger.debug("展示用户的所有文章。。。")
    user_id = request.session['loginUser'].id
    articles = models.Article.objects.filter(author=user_id).order_by("-publicTime")
    # print(articles[0].title)
    for article in articles:
        reg = r'<[^>]+>'
        article.content = re.sub(reg, '', article.content)
    return render(request, "blog/self_all_article.html", {"articles": articles})


def code(request):
    """
    生成验证码
    :param request: 请求头对象
    :return:
    """
    img, code = utils.create_code()
    # 将code保存到session中
    request.session['code'] = code
    # 返回图片
    file = BytesIO()
    img.save(file, 'PNG')
    return HttpResponse(file.getvalue(), "image/png")


def check_nickname(request, nickname):
    qs = models.User.objects.filter(nickname=nickname)
    if len(qs) > 0:
        return JsonResponse({"n_msg": "该用户名已存在", "success": False})
    else:
        return JsonResponse({"n_msg": "用户名可用", "success": True})