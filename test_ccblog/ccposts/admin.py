#coding:utf-8
from pagedown.widgets import AdminPagedownWidget
from django.contrib import admin
from django.db import models
from .models import Tag, Article, ArticleImage, Category


# 标签模型后台管理
class TagAdmin(admin.ModelAdmin):
    list_display = ('tagname', 'articlecount')

# 标签模型后台管理注册
admin.site.register(Tag, TagAdmin)


# 博文模型后台管理
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_time','last_modified_time','status')
    formfield_overrides = {
            models.TextField: {'widget': AdminPagedownWidget},}


# 博文模型后台管理注册
admin.site.register(Article, ArticleAdmin)


# 博文图片模型后台管理
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'image', 'upload_time')

# 博文图片模型后台管理注册
admin.site.register(ArticleImage, ArticleImageAdmin)


# 博文目录模型后台管理
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryname', 'articlecount','last_modified_time', 'created_time')
admin.site.register(Category, CategoryAdmin)

