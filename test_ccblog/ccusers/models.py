# coding:utf-8
from __future__ import unicode_literals
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.signals import user_logged_in
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
# code_generator 发送账号激活邮箱待解决！


class MyUserManager(UserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('你需要一个邮箱')

        user = self.model(
            username=self.normalize_username(username),
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.extra_fields.setdefault('is_staff', True)
        user.extra_fields.setdefault('is_superuser', True)
        user.extra_fields.setdefault('is_admin', True)
        user.extra_fields.setdefault('is_active', True)
        user.save(using=self._db)
        return user

USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'


class MyUser(AbstractUser):
    username = models.CharField(max_length=150,
                                validators=[
                                    RegexValidator(
                                        regex=USERNAME_REGEX,
                                        message='Required. Username must be Alphanumeric or contain any of the following: ".@+-"',
                                        code='invalid_username'
                                    )],
                                unique=True,
                                )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(verbose_name="账号状态", default=False)
    is_staff = models.BooleanField(verbose_name="员工状态", default=False)
    is_admin = models.BooleanField(verbose_name="系统管理员状态", default=False)
    date_joined = models.DateTimeField(verbose_name="加入日期", default=timezone.now)
    last_login = models.DateTimeField(verbose_name="最近登录", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm_list, obj=None):
        # Does the User have a specific permission?
        # Simplest possible answer: Yes, always
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        # return _user_has_module_perms(self, app_label)


def update_last_login(sender, MyUser, **kwargs):
    MyUser.last_login = timezone.now()
    MyUser.save(update_fields=['last_login'])

user_logged_in.connect(update_last_login, sender=MyUser)


class ActivationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    key = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
    #    self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)


def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print('activation created')

post_save.connect(post_save_activation_receiver, sender=ActivationProfile)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    city = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):
        return str(self.user.username)


def post_save_user_model_receiver(sender, instance, created, *args,**kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

















