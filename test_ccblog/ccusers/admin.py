#coding:utf-8
from django import forms
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .forms import UserCreationForm, UserChangeForm
from .models import MyUser, Profile, ActivationProfile


class MyUserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email','password')}),
        ('Personal info', {'fields': ('zipcode',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff',)}),
        ('Access', {'fields': ('is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','password1','password2')}
         ),
    )
    search_fields = ('username','email',)
    ordering = ('username', 'email',)
    filter_horizontal = ()

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile)
admin.site.register(ActivationProfile)

# admin.site.unregister(Group)
