from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="IDEEZA Analytics API",
        default_version="v1",
        description="The API for IDEEZA Analytics",
        terms_of_service="https://www.ideeza.com/policies/terms/",
        contact=openapi.Contact(email="yeabsera.dev@gmail.com"),
        license=openapi.License(name="MIT Software License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_v1_patterns = [
    path("", include(("core.api.urls", "api"), namespace="api")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_patterns)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa

urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)
