#coding:utf-8
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

# “邮件密码重置”部分采用了django内置的模块，为了和登录注册统一，让整套Authentication系统呈现得更清楚，
# 此部分urls放在本应用（ccusers.urls）下，相应templates放在模板文件夹ourusers（templates/ccusers）下，即auth_views中相应模板路径全部需要修改！！！
# 而auth_views中类似reverse('password_reset_done')部分也须修改成reverse('ccusers:password_reset_done')，否则会返回reverse错误！！！

app_name = 'ccusers'

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^register/$', views.register, name='register'),
    url('^logout/$', views.logout_view, name='logout'),
    url('^register_activate/activation/$', views.activate_view, name='activation'),
    url(r'^register_guide_message/$', views.activate_guide_view, name='activate_guide'),
    # url(r'^activate/(?P<code>[a-z0-9].*)/$', views.activate_user_view, name="user_activate"),
    url('^login/$', views.login_view, name='login'),
    url(r'^reset_password/$', auth_views.password_reset, name='password_reset'),
    url(r'^reset_password/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset_password/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),

]
