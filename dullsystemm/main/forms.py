from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

# Стандартные поля регистрации создаём в форме

from .models import *
# Регистрация пользователей
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Стандартное поле для авторизации
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

# Отзывы
class CommentForm(forms.ModelForm):
    body = forms.CharField(label='Отзыв', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Comments_User
        fields = ('body',)

# Новости
class CommentFormNews(forms.ModelForm):
    body = forms.CharField(label='Комментарий', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Comments_news
        fields = ('body',)


