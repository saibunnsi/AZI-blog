#coding:utf-8
from django import template
from django.core.paginator import (Paginator,
        PageNotAnInteger, EmptyPage)
#分类功能涉及的类和异常

register = template.Library()
#定义模板标签需要

@register.simple_tag(takes_context=True)
#装饰器的作用是表明此函数是一个模板标签
#take_context=True表示接受上下文对象，即封装了各种变量的Context对象

def paginate(context, object_list, page_count):
    #context是Context对象，object_list是要分页的对象，page_count是表示每页的数量
    left = 3
    right = 3
    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page')

    try:
        object_list = paginator.page(page)
        context['current_page'] = int(page)
        pages = get_left(context['current_page'], left, paginator.num_pages) + get_right(context['current_page'], right, paginator.num_pages)
    except PageNotAnInteger:
        object_list = paginator.page(1)
        context['current_page'] = 1
        pages = get_right(context['current_page'], right, paginator.num_pages)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = get_left(context['current_page'], left, paginator.num_pages)

    context['article_list'] = object_list
    context['pages'] = pages
    context['last_page'] = paginator.num_pages
    context['first_page'] = 1

    try:
        context['pages_first'] = pages[0]
        context['pages_last'] = pages[-1] + 1
    except IndexError:
        context['pages_first'] = 1
        context['pages_last'] = 2
    return ''

def get_left(current_page, left, num_pages):
    if current_page == 1:
        return []
    elif current_page == num_pages:
        l = [i - 1 for i in range(current_page, current_page - left, -1) if i -1 > 1]
        l.sort()
        return l
    l = [i for i in range(current_page, current_page - left, -1) if i > 1]
    l.sort()
    return l

def get_right(current_page, right, num_pages):
    if current_page == num_pages:
        return []
    return [i + 1 for i in range(current_page, current_page + right - 1) if
            i < num_pages - 1]
