from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path("analytics/", include(("core.analytics.urls", "analytics"), namespace="analytics")),
]
