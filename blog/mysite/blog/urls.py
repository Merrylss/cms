from django.conf.urls import url

from . import views

# app_name = "blog"

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^reg_user/$', views.reg_user, name='reg_user'),
    url(r'^log_user/$', views.log_user, name='log_user'),
    url(r'^out_user/$', views.out_user, name='out_user'),
    # url(r'^(\d+)del_user/$', views.del_user, name='del_user'),
    url(r'^del_user/(?P<user_id>\d+)/$', views.del_user, name='del_user'),
    url(r'^all_user/$', views.all_user, name='all_user'),
    url(r'^login_success/$', views.login_success, name='login_success'),
    url(r'^show_user/(\d+)/$', views.show_user, name='show_user'),
    url(r'^(?P<user_id>\d+)/change_info/$', views.change_info, name='change_info'),
    url(r'^user_change_info/$', views.user_change_info, name='user_change_info'),
    # 文章操作
    url(r'^add_article/$', views.add_article, name='add_article'),
    url(r'^(?P<a_id>\d+)/del_article/$', views.del_article, name='del_article'),
    url(r'^(?P<a_id>\d+)/update_article/$', views.update_article, name='update_article'),
    url(r'^(?P<a_id>\d+)/show_article/$', views.show_article, name='show_article'),
    url(r'^(?P<a_id>\d+)/only_show_article/$', views.only_show_article, name='only_show_article'),
    url(r'^self_all_article/$', views.self_all_article, name='self_all_article'),
    # 验证码
    url(r'^code/$', views.code, name='code'),
    url(r'^(\w+)/check_nickname/$', views.check_nickname, name='check_nickname'),
    # ajax

]