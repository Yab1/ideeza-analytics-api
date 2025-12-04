from typing import Any, Dict, List, Literal

from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear

from core.analytics.filters import DynamicFilterBuilder
from core.analytics.models import BlogView


def blog_views_get_grouped_metrics(
    *,
    object_type: Literal["country", "user"],
    range_type: Literal["month", "week", "year"],
    filters: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """
    Get grouped blog view metrics.

    Groups BlogView records by object_type (country or user) and time range.
    Returns metrics with x (grouping key), y (number of unique blogs), z (total views).

    Args:
        object_type: Group by "country" or "user"
        range_type: Time grouping - "month", "week", or "year"
        filters: Optional dynamic filter dictionary

    Returns:
        List of dicts with keys: x (grouping key), y (number of blogs), z (total views)
    """
    queryset = BlogView.objects.select_related("blog", "viewer_user", "viewer_country")

    if filters:
        q_filter = DynamicFilterBuilder.build(filters)
        queryset = queryset.filter(q_filter)

    trunc_map = {
        "month": TruncMonth("viewed_at"),
        "week": TruncWeek("viewed_at"),
        "year": TruncYear("viewed_at"),
    }
    trunc_func = trunc_map.get(range_type, TruncMonth("viewed_at"))

    queryset = queryset.annotate(period=trunc_func)

    if object_type == "country":
        results = (
            queryset.values("period", "viewer_country__code")
            .annotate(
                y=Count("blog", distinct=True),
                z=Count("id"),
            )
            .order_by("period", "viewer_country__code")
        )

        formatted_results = []
        for result in results:
            country_code = result["viewer_country__code"] or "Unknown"
            formatted_results.append({
                "x": country_code,
                "y": result["y"],
                "z": result["z"],
            })
    else:
        results = (
            queryset.values("period", "viewer_user__id")
            .annotate(
                y=Count("blog", distinct=True),
                z=Count("id"),
            )
            .order_by("period", "viewer_user__id")
        )

        formatted_results = []
        for result in results:
            user_id = result["viewer_user__id"]
            if user_id is None:
                user_id = "Unknown"
            else:
                user_id = str(user_id)
            formatted_results.append({
                "x": user_id,
                "y": result["y"],
                "z": result["z"],
            })

    return formatted_results
