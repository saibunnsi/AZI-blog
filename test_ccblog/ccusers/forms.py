# coding: utf-8
from django import forms
from django.db.models import Q
from django.core.validators import RegexValidator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, get_user_model
from .models import USERNAME_REGEX

User = get_user_model()


class UserCreationForm(forms.ModelForm, SuccessMessageMixin):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    success_url = '/success/'
    success_message = "Successfully created!"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.changed_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):

    query = forms.CharField(label='Username/Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get("query")
        password = self.cleaned_data.get("password")
        user_qs_final = User.objects.filter(
            Q(username__iexact=query)|
            Q(email__iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count() != 1:
            raise forms.ValidationError("Invalid credentials -- user does not exist!")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("Invalid credentials. -- password invalid!")
        if not user_obj.is_active:
            raise forms.ValidationError("Inactive user. Please verify your email address.")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff', 'is_active')

    def cleaned_password(self):
        return self.initial["password"]
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value.
