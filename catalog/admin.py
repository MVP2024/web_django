from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, ContactInfo, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Административный класс для модели Category.
    Настраивает отображение и поиск категорий в админке.
    """

    list_display = ("id", "name", "image_display")
    search_fields = ("name",)

    def image_display(self, obj):
        """Отображает миниатюру изображения категории в списке админки."""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "-"

    image_display.short_description = "Изображение категорий"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административный класс для модели Product.
    Настраивает отображение, фильтрацию и поиск продуктов в админке.
    """

    list_display = ("id", "name", "price", "category", "image_display")
    list_filter = ("category",)
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")

    def image_display(self, obj):
        """Отображает миниатюру изображения продукта в списке админки."""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "-"

    image_display.short_description = "Изображение"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """
    Административный класс для модели ContactInfo.
    Настраивает отображение контактной информации в админке.
    """

    list_display = ("country", "inn", "address")
