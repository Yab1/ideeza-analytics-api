import json
from typing import Literal, cast

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.analytics.selectors import blog_views_get_grouped_metrics


class BlogViewsApi(APIView):
    class InputSerializer(serializers.Serializer):
        object_type = serializers.ChoiceField(choices=["country", "user"], required=True)
        range = serializers.ChoiceField(choices=["month", "week", "year"], required=True)
        filters = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class OutputSerializer(serializers.Serializer):
        x = serializers.CharField()
        y = serializers.IntegerField()
        z = serializers.IntegerField()

    @swagger_auto_schema(
        operation_summary="Get blog views grouped metrics",
        operation_description="Retrieve blog views metrics grouped by the specified object type and time range.",
        manual_parameters=[
            openapi.Parameter(
                "object_type",
                openapi.IN_QUERY,
                description="Type of object to group by",
                type=openapi.TYPE_STRING,
                enum=["country", "user"],
                required=True,
            ),
            openapi.Parameter(
                "range",
                openapi.IN_QUERY,
                description="Time range for grouping",
                type=openapi.TYPE_STRING,
                enum=["month", "week", "year"],
                required=True,
            ),
            openapi.Parameter(
                "filters",
                openapi.IN_QUERY,
                description="Optional JSON string for additional filters",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successfully retrieved blog views metrics",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "x": openapi.Schema(type=openapi.TYPE_STRING, description="Group identifier"),
                            "y": openapi.Schema(type=openapi.TYPE_INTEGER, description="Metric value"),
                            "z": openapi.Schema(type=openapi.TYPE_INTEGER, description="Additional metric value"),
                        },
                    ),
                ),
            ),
            400: openapi.Response(description="Bad request - Invalid parameters"),
        },
    )
    def get(self, request):
        input_serializer = self.InputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        validated_data = cast(dict[str, str | None], input_serializer.validated_data)

        filters = None
        filters_str = validated_data.get("filters")
        if filters_str:
            try:
                filters = json.loads(filters_str)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"filters": "Invalid JSON format"})

        data = blog_views_get_grouped_metrics(
            object_type=cast(Literal["country", "user"], validated_data["object_type"]),
            range_type=cast(Literal["month", "week", "year"], validated_data["range"]),
            filters=filters,
        )

        output_serializer = self.OutputSerializer(data, many=True)

        return Response(data=output_serializer.data, status=status.HTTP_200_OK)
