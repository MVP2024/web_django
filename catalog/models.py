from django.db import models
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование', unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование', unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(upload_to='product/%Y/%m, %d', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за покупку', null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f"{self.image}  {self.name} {self.price}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

