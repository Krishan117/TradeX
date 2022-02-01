from django import forms
from django.forms import ModelForm,fields
from django.contrib.auth.models import User
from myapp.models import *

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','password')