from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.exceptions import PermissionDenied
from .models import Category, ContactInfo, Product


class ImageDisplayLogicMixin:
    # Этот метод содержит многократно используемую логику для генерации HTML изображения
    @staticmethod
    def _get_image_html(obj) -> str:
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "-"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ImageDisplayLogicMixin):
    list_display = ("id", "name", "image_display")
    search_fields = ("name",)

    def image_display(self, obj) -> str:
        if obj.image:
            return self._get_image_html(obj)

    image_display.short_description = "Изображение категорий"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ImageDisplayLogicMixin):
    list_display = ("id", "name", "price", "category", "owner", "image_display")
    list_filter = ("category", "owner")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    actions = ["unpublish_selected_products"]

    def unpublish_selected_products(self, request, queryset):
        if not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied
        queryset.update(is_published=False)

    unpublish_selected_products.short_description = "Отменить публикацию выбранных продуктов"

    def image_display(self, obj) -> str:
        if obj.image:
            return self._get_image_html(obj)

    image_display.short_description = "Изображение"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("country", "inn", "address")
