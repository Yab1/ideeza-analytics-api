from typing import Any, Dict, List, Literal

from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek, TruncYear

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


def top_get_ranked(
    *,
    top_type: Literal["user", "country", "blog"],
    start_date: str | None = None,
    end_date: str | None = None,
    filters: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """
    Get top 10 ranked entities by view count.

    Args:
        top_type: Rank by "user", "country", or "blog"
        start_date: Optional start date for time range (ISO format)
        end_date: Optional end date for time range (ISO format)
        filters: Optional dynamic filter dictionary

    Returns:
        List of dicts with keys: x, y, z (varies by top_type)
        - top=user: x=blogs, y=views, z=countries
        - top=country: x=users, y=views, z=blogs
        - top=blog: x=users, y=views, z=countries
    """
    from django.utils import timezone
    from django.utils.dateparse import parse_datetime

    queryset = BlogView.objects.select_related("blog", "viewer_user", "viewer_country")

    if start_date:
        if "T" not in start_date:
            start_date = f"{start_date}T00:00:00Z"
        start_dt = parse_datetime(start_date)
        if start_dt:
            if timezone.is_naive(start_dt):
                start_dt = timezone.make_aware(start_dt)
            queryset = queryset.filter(viewed_at__gte=start_dt)

    if end_date:
        if "T" not in end_date:
            end_date = f"{end_date}T23:59:59Z"
        end_dt = parse_datetime(end_date)
        if end_dt:
            if timezone.is_naive(end_dt):
                end_dt = timezone.make_aware(end_dt)
            queryset = queryset.filter(viewed_at__lte=end_dt)

    if filters:
        q_filter = DynamicFilterBuilder.build(filters)
        queryset = queryset.filter(q_filter)

    if top_type == "user":
        results = (
            queryset.values("viewer_user__id")
            .annotate(
                x=Count("blog", distinct=True),
                y=Count("id"),
                z=Count("viewer_country", distinct=True),
            )
            .order_by("-y")[:10]
        )

        formatted_results = []
        for result in results:
            if result["viewer_user__id"] is None:
                continue
            formatted_results.append({
                "x": result["x"],
                "y": result["y"],
                "z": result["z"],
            })

    elif top_type == "country":
        results = (
            queryset.values("viewer_country__code")
            .annotate(
                x=Count("viewer_user", distinct=True),
                y=Count("id"),
                z=Count("blog", distinct=True),
            )
            .order_by("-y")[:10]
        )

        formatted_results = []
        for result in results:
            if result["viewer_country__code"] is None:
                continue
            formatted_results.append({
                "x": result["x"],
                "y": result["y"],
                "z": result["z"],
            })

    else:
        results = (
            queryset.values("blog__id", "blog__title")
            .annotate(
                x=Count("viewer_user", distinct=True),
                y=Count("id"),
                z=Count("viewer_country", distinct=True),
            )
            .order_by("-y")[:10]
        )

        formatted_results = []
        for result in results:
            formatted_results.append({
                "x": result["x"],
                "y": result["y"],
                "z": result["z"],
            })

    return formatted_results


def performance_get_time_series(
    *,
    compare_type: Literal["day", "week", "month", "year"],
    user_id: str | None = None,
    filters: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """
    Get time-series performance metrics.

    Args:
        compare_type: Time period grouping - "day", "week", "month", or "year"
        user_id: Optional user ID to filter by specific user's blogs
        filters: Optional dynamic filter dictionary

    Returns:
        List of dicts with keys: x (period label + blog count), y (views), z (growth %)
    """
    from datetime import datetime

    queryset = BlogView.objects.select_related("blog", "blog__user", "viewer_user", "viewer_country")

    if user_id:
        queryset = queryset.filter(blog__user_id=user_id)

    if filters:
        q_filter = DynamicFilterBuilder.build(filters)
        queryset = queryset.filter(q_filter)

    trunc_map = {
        "day": TruncDay("viewed_at"),
        "week": TruncWeek("viewed_at"),
        "month": TruncMonth("viewed_at"),
        "year": TruncYear("viewed_at"),
    }
    trunc_func = trunc_map.get(compare_type, TruncMonth("viewed_at"))

    results = (
        queryset.annotate(period=trunc_func)
        .values("period")
        .annotate(
            blog_count=Count("blog", distinct=True),
            view_count=Count("id"),
        )
        .order_by("period")
    )

    formatted_results = []
    previous_views = None

    for result in results:
        period = result["period"]
        blog_count = result["blog_count"]
        view_count = result["view_count"]

        if period is None:
            continue

        if isinstance(period, datetime):
            if compare_type == "day":
                period_label = period.strftime("%Y-%m-%d")
            elif compare_type == "week":
                year, week, _ = period.isocalendar()
                period_label = f"{year}-W{week:02d}"
            elif compare_type == "month":
                period_label = period.strftime("%Y-%m")
            else:
                period_label = period.strftime("%Y")
        else:
            period_label = str(period)

        x = f"{period_label} ({blog_count} blogs)"

        if previous_views is not None and previous_views > 0:
            growth = ((view_count - previous_views) / previous_views) * 100
            z = round(growth, 2)
        elif previous_views is not None and previous_views == 0:
            z = 100.0 if view_count > 0 else 0.0
        else:
            z = 0.0

        formatted_results.append({
            "x": x,
            "y": view_count,
            "z": z,
        })

        previous_views = view_count

    return formatted_results
