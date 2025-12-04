from django.contrib import admin

from core.analytics.models import Blog, BlogView, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "created_at"]
    search_fields = ["name", "code"]
    ordering = ["name"]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "country", "created_at"]
    list_filter = ["country", "created_at"]
    search_fields = ["title"]
    raw_id_fields = ["user", "country"]
    date_hierarchy = "created_at"


@admin.register(BlogView)
class BlogViewAdmin(admin.ModelAdmin):
    list_display = ["blog", "viewer_user", "viewer_country", "viewed_at"]
    list_filter = ["viewer_country", "viewed_at"]
    raw_id_fields = ["blog", "viewer_user", "viewer_country"]
    date_hierarchy = "viewed_at"
    readonly_fields = ["viewed_at"]
