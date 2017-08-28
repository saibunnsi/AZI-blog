#coding:utf-8
from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'user', 'created_time')


admin.site.register(Comment, CommentAdmin)