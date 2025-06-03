from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей, где email является уникальным идентификатором
    для аутентификации вместо username.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email должно быть установлено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # Переопределяем поле email, чтобы оно было уникальным и использовалось для авторизации
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    # Переопределяем username, чтобы сделать его необязательным
    username = models.CharField(
        max_length=150,
        unique=False,
        null=True,
        blank=True,
        verbose_name="Имя пользователя"
    )

    # Дополнительные поля
    avatar = models.ImageField(
        upload_to="users/avatars/",
        null=True,
        blank=True,
        verbose_name="Аватар"
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Номер телефона"
    )
    country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Страна"
    )

    # Указываем, что для авторизации используется поле email
    USERNAME_FIELD = 'email'
    # Указываем, какие поля обязательны при создании суперпользователя (кроме USERNAME_FIELD и password)
    REQUIRED_FIELDS = []

    # Привязываем наш кастомный менеджер к модели User
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
