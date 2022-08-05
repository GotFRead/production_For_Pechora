from django import forms
from django.contrib.auth.forms import AuthenticationForm,  UserCreationForm
from django.contrib.auth.models import User
from django.views import generic
from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input',
                                                             'placeholder': 'Введите логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input',
                                                                 'placeholder': 'Введите пароль'}))


class RigistrForm(generic.CreateView):

    form_class = User

    first_name = forms.CharField(widget=forms.TextInput({'class': 'input',
                                                             'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput({'class': 'input',
                                                         'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input',
                                                             'placeholder': 'Введите логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input',
                                                                 'placeholder': 'Введите пароль'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input',
                                                                  'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'username', 'password'}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class Registr(UserCreationForm):
    form_class = User
