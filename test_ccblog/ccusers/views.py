# coding:utf-8
from django.shortcuts import render
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.core.mail import send_mail

from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect

from .forms import UserCreationForm, UserLoginForm
from .models import ActivationProfile, MyUser

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            save_it = form.save()
            save_it.save()
            id_ = save_it.id
            to_mail = save_it.email
            from_email = settings.EMAIL_HOST_USER
            to_list = [to_mail, id_, from_email]
            text = "Hi\nHow's it going?\n Here is the for you to activate your account:\n" \
                   "http://127.0.0.1:8000/ccusers/register_activate/activation/?id=%s" %(id_)
            part1 = MIMEText(text, 'plain')
            message = MIMEMultipart('alternative')
            message.attach(part1)
            subject = "Please activate your account at AZI blog!"
            message = """\nFrom: %s\nTo: %s\nSubject: %s\n\n%s """ % (from_email, to_mail, subject, message.as_string())
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            messages.success(request, 'Thanks for your registration. Have a good day!')
            return redirect('../../ccusers/register_guide_message')

        else:
            form = UserCreationForm()
        return render(request, 'ccusers/register.html', context={'form': form})


def activate_guide_view(request):
    return render(request, 'ccusers/register_activation_guide.html')


def activate_view(request):
    id_ = int(request.GET.get('id'))
    user = MyUser.objects.get(id=id_)
    user.is_active = True
    user.save()
    return render(request, 'ccusers/register_activation_complete.html')


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        act_profile_qs = ActivationProfile.objects.filter(key=code)
        if act_profile_qs.exists() and act_profile_qs.count == 1:
            act_obj = act_profile_qs.first()
            if not act_obj.expired:
                user_obj = act_obj.user
                user_obj.is_active = True
                user_obj.save()
                act_obj.expired = True
                act_obj.save()
                return HttpResponseRedirect("/login")
    return HttpResponseRedirect("/login")


def login_view(request, *args, **kwargs):
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        if redirect_to:
            return redirect(redirect_to)
        else:
            return redirect('../../ccposts/')
    return render(request, "ccusers/login.html", context={'form': form, 'next':redirect_to})


def logout_view(request):
    redirect_to = request.GET.get('next', request.GET.get('next',''))
    logout(request)
    if redirect_to:
        return redirect(redirect_to)
    else:
        return redirect('/')













