from django.urls import path

from core.analytics.apis import BlogViewsApi

app_name = "analytics"

urlpatterns = [
    path("blog-views/", BlogViewsApi.as_view(), name="blog-views"),
]
