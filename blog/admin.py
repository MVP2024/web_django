from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at", "views_count")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
    readonly_fields = ("created_at", "views_count")
