#coding:utf-8
from __future__ import unicode_literals

import os
import datetime
import secretballot

from django.db import models
from django.db.models import IntegerField
from django.utils import timezone

from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from collections import defaultdict

#delete md_file before delete/change model
from django.conf import settings
from django.db.models.signals import pre_delete
from django.db.models import F

from django.dispatch import receiver
from django.core.files.base import ContentFile

import unidecode
from taggit.managers import TaggableManager

from django.contrib.contenttypes.models import ContentType
from comments.models import Comment


class TagManager(models.Manager):
    @property
    def get_tag_list(self):
        tags = Tag.objects.all()
        taglist = []
        for i in range(len(tags)):
            taglist.append([])
        for i in range(len(tags)):
            temp = Tag.objects.get(tagname=tags[i])
            posts = temp.article_set.all()
            taglist[i].append(tags[i].tagname)
            taglist[i].append(len(posts))
        return taglist

class Tag(models.Model):
    class Meta:
        ordering = ['tagname']

    objects = models.Manager()
    tagname = models.CharField(verbose_name='标签名',max_length=30)
    tag_list = TagManager()
    articlecount = models.PositiveIntegerField(verbose_name='标签下文章数',default=0)

    def __unicode__(self):
        return self.tagname


upload_dir = 'content/Article/%s/%s'


def get_upload_md_name(self, filename):
    if self.created_time:
        year = self.created_time.year
    else:
        year = datetime.now().year
        upload_to = upload_dir % (year, self.title + '.md')
        return upload_to


def get_html_name(self, filename):
    if self.created_time:
        year = self.created_time.year
    else:
        year = datetime.now().year
        upload_to = upload_dir % (year, filename)
        return upload_to


class ArticleManager(models.Manager):
    def archive(self):
        date_list = Article.objects.datetimes('created_time','month','day',order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items(), reverse=True)


class Article(models.Model):
    class Meta:
        ordering = ['-last_modified_time']

    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    objects = ArticleManager()
    title = models.CharField(verbose_name='标题', max_length=150)
    body = models.TextField(verbose_name='正文', blank=True)
    abstract = models.CharField(verbose_name='摘要', max_length=200, blank=True, help_text="如无，截取文章前200字！")
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    last_modified_time = models.DateTimeField(verbose_name='上次修改时间', auto_now=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    category = models.ForeignKey('Category', verbose_name='目录')
    status = models.CharField(verbose_name='文章状态', max_length=1, choices=STATUS_CHOICES)
    slug = models.SlugField(unique=True)
    commentcount = models.PositiveIntegerField(verbose_name='评论数', blank=True, default=0)
    views = models.PositiveIntegerField(verbose_name='浏览量', blank=True, default=0)
    likes = models.PositiveIntegerField(verbose_name='点赞数', blank=True, default=0)
    topped = models.NullBooleanField(verbose_name='置顶', default=True)
    html_file = models.FileField(verbose_name='上传html文件', upload_to=get_html_name, blank=True)
    md_file = models.FileField(verbose_name='上传md文件', upload_to=get_upload_md_name, blank=True)

    # 点击提交评论表单后，返回当前页面！
    def get_absolute_url(self):
        return reverse('ccposts:detail', kwargs={'slug': self.slug})

    def gettags(self):
        tag = self.tags.all()
        return tag

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
        return self.views

    #用于交互解释器显示表示该类的字符串
    def __unicode__(self):
        return self.title

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_models(instance.__class__)
        return content_type


secretballot.enable_voting_on(Article)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def get_upload_img_name(self, filename):
    upload_to = upload_dir % ('images', filename)
    return upload_to

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name="images")
    image = models.ImageField(upload_to=get_upload_img_name)
    upload_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)


class Category(models.Model):
    categoryname = models.CharField(verbose_name='目录名称',max_length=30)
    articlecount = models.PositiveIntegerField(verbose_name='文章篇数', default=0)
    created_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def __unicode__(self):
        return self.categoryname