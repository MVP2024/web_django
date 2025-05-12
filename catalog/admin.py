from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, ContactInfo, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image_display")
    search_fields = ("name",)

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "-"

    image_display.short_description = "Изображение категорий"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "image_display")
    list_filter = ("category",)
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "-"

    image_display.short_description = "Изображение"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("country", "inn", "address")
