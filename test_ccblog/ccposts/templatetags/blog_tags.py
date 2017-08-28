#coding:utf-8
from django import template
from django.db.models.aggregates import Count
from ccposts.models import Article, Category, Tag
register = template.Library()

@register.simple_tag
def get_hottest_articles(num=6):
    return Article.objects.all().order_by('-views')[:num]

@register.simple_tag
def get_recent_articles(num=6):
    return Article.objects.all().order_by('-last_modified_time')[:num]

@register.simple_tag
def archives():
    return Article.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('article')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('article')).filter(num_posts__gt=0)
#Line 26无字符 运行服务器时却一直出错，删到Line 24时，重启正确！？？？？简直有毛病好吗！！！浪费我一下午的时间！！！

from django.utils.safestring import mark_safe
import json
@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))