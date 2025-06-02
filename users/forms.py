from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # Указываем поля, которые будут использоваться при создании пользователя
        # Исключаем 'username', так как авторизация идет по email
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country', 'password', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        # Указываем поля, которые будут доступны для изменения в админке
        # Исключаем 'username', так как авторизация идет по email
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country',
                  'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')