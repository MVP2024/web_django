from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование", unique=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    image = models.ImageField(upload_to="categories/%Y/%m/%d/", verbose_name="Изображение", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование", unique=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    image = models.ImageField(upload_to="product/%Y/%m/%d", verbose_name="Изображение", null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name="Цена за покупку",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", related_name="products", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.image}  {self.name} {self.price}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]
        permissions = [
            ("can_unpublish_product", "Может отменить публикацию продукта"),
        ]


class ContactInfo(models.Model):
    country = models.CharField(max_length=100, verbose_name="Страна")
    inn = models.CharField(max_length=20, verbose_name="ИНН")
    address = models.TextField(verbose_name="Адрес")

    def __str__(self) -> str:
        return f"Контакты: {self.address}"

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"