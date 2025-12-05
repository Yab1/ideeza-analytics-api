from django.urls import path

from core.analytics.apis import BlogViewsApi, PerformanceApi, TopApi

app_name = "analytics"

urlpatterns = [
    path("blog-views/", BlogViewsApi.as_view(), name="blog-views"),
    path("top/", TopApi.as_view(), name="top"),
    path("performance/", PerformanceApi.as_view(), name="performance"),
]
