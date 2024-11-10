from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "post",
        "views_count",
        "created_at",
        "updated_at",
        "is_published",
    )
    list_filter = ("title", "views_count", "created_at")
    search_fields = (
        "title",
        "created_at",
    )
