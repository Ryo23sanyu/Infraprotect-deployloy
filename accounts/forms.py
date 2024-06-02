from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from infra.models import CustomUser


class SignupForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ('username',)# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #

from django import forms
from .models import Company,CustomUser

class CompanyForm(forms.ModelForm):
  class Meta:
    model	= Company
    fields	= [ "name" ]

class CustomUserForm(forms.ModelForm):
  class Meta:
    model	= CustomUser
    fields	= [ "name" ]

# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #

from django import forms
from .models import Company,CustomUser

class CompanyForm(forms.ModelForm):
    class Meta:
        model	= Company
        fields	= [ "name" ]

class CustomUserForm(forms.ModelForm):
    class Meta:
        model	= CustomUser
        fields	= [ "name" ]

