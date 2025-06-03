
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Поля, отображаемые в списке пользователей в админке
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'phone', 'country')
    # Фильтры для списка пользователей
    list_filter = ('is_staff', 'is_active', 'country')
    # Поля для поиска
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    # Сортировка по умолчанию
    ordering = ('email',)

    # Настройка полей для формы редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'avatar', 'phone', 'country')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    # Настройка полей для формы создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'avatar', 'phone', 'country')}
        ),
    )
