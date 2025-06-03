from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # UserCreationForm автоматически обрабатывает поля USERNAME_FIELD (email) и пароль.
        # Здесь нужно указывать только дополнительные поля, которые вы добавили в модель User.
        fields = (
            "email",
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "country",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        # Для формы изменения пользователя можно явно перечислить все поля,
        # которые вы хотите сделать доступными для редактирования.
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "country",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


# Новая форма для редактирования профиля пользователя
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "country",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }
