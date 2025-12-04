from typing import Any, Dict

from django.db.models import Q


class DynamicFilterBuilder:
    """Builds Django Q objects from nested filter structures."""

    OPERATORS = {
        "eq": lambda field, value: Q(**{field: value}),
        "ne": lambda field, value: ~Q(**{field: value}),
        "gt": lambda field, value: Q(**{f"{field}__gt": value}),
        "gte": lambda field, value: Q(**{f"{field}__gte": value}),
        "lt": lambda field, value: Q(**{f"{field}__lt": value}),
        "lte": lambda field, value: Q(**{f"{field}__lte": value}),
        "in": lambda field, value: Q(**{f"{field}__in": value}),
        "contains": lambda field, value: Q(**{f"{field}__icontains": value}),
    }

    @classmethod
    def build(cls, filter_dict: Dict[str, Any]) -> Q:
        """
        Recursively builds Q objects from filter structure.

        Supports: and, or, not, eq, ne, gt, gte, lt, lte, in, contains
        """
        if not filter_dict:
            return Q()

        q_objects = Q()

        if "and" in filter_dict:
            and_q = Q()
            for condition in filter_dict["and"]:
                and_q &= cls.build(condition)
            q_objects &= and_q

        if "or" in filter_dict:
            or_q = Q()
            for condition in filter_dict["or"]:
                or_q |= cls.build(condition)
            q_objects |= or_q

        if "not" in filter_dict:
            not_q = Q()
            for condition in filter_dict["not"]:
                not_q |= cls.build(condition)
            q_objects &= ~not_q

        if "field" in filter_dict:
            field = filter_dict["field"]
            for op, func in cls.OPERATORS.items():
                if op in filter_dict:
                    value = filter_dict[op]
                    q_objects &= func(field, value)

        return q_objects
