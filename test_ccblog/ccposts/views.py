#coding:utf-8


from collections import defaultdict
from math import ceil
from os.path import join

import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed

from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponse, Http404
from django.shortcuts import (render, render_to_response, redirect,
    get_object_or_404, HttpResponseRedirect, HttpResponse)
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
from django.template import loader, Context

from .models import (Article, Category, Tag,
    TagManager, ArticleImage)

from comments.models import Comment
from comments.forms import CommentForm


def page_not_found(request):
    return render_to_response('ccposts/404.html')
def page_error(request):
    return render_to_response('ccposts/500.html')

def search_titles(request):
    posts = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text',''))
    return render_to_response('search/ajax_search.html', {'posts:posts'})
def index(request):
    article_list = Article.objects.all().order_by('-last_modified_time')[0:1]
    return render(request, 'ccposts/index.html', context={'article_list':article_list})

def ArticleDetailView(request, slug=None):
    instance = get_object_or_404(Article, slug=slug)
    initial_data = {"content_type": instance.get_content_type, "object_id": instance.id }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
                        user = request.user,
                        content_type = content_type,
                        object_id = obj_id,
                        content = content_data,
                        parent = parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    comments = instance.comments

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite(linenums=True)',
        'markdown.extensions.toc',
        TocExtension(slugify=slugify, permalink=True)
    ])
    instance.body = md.convert(instance.body)

    context = {
        "title": instance.title,
        "instance": instance,
        "toc": md.toc,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, 'ccposts/detail.html', context=context)

class Archive(generic.ListView):
    model = Article
    template_name = "ccposts/archive.html"
    context_object_name = "article_list"

def archives(request, year, month):
    article_list = Article.objects.filter(created_time__year=year).order_by('-last_modified_time')
    context={'article_list': article_list}
    return render(request, 'ccposts/archivebydate.html', context)

def AboutMe(request):
    return render(request, 'ccposts/aboutme.html')

class RSSFeed(Feed):
    title = "AZI's blog"
    link = "ccposts/RSS/"
    description = "阿滋的博文RSS Feed"
    def items(self):
        return Article.objects.order_by('-last_modified_time')
    def item_title(self, item):
        return item.title
    def item_last_modified_time(self, item):
        return item.last_modified_time
    def item_description(self, item):
        return item.body

class TagView(generic.ListView):
    model = Article
    template_name = "ccposts/tag.html"
    context_object_name = "article_list"

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

class CategoryView(generic.ListView):
    model = Article
    template_name = "ccposts/category.html"
    context_object_name = "article_list"
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
