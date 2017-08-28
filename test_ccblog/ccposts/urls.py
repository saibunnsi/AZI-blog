from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<slug>[\w-]+)/$', views.ArticleDetailView, name='detail'),
    url(r'^archive/$', views.Archive.as_view(), name='archive'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives, name='archivebydate'),
    url(r'^aboutme/$', views.AboutMe, name='aboutme'),
    url(r'^RSS/$', views.RSSFeed(), name='RSS'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view, name='category'),
    url(r'^ajax_search/$', views.search_titles, name='ajax_search'),
    ]
