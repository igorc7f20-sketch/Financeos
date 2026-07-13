from django.db.models import Sum
from django.db.models.functions import TruncMonth

from apps.cash.models import CashMovement


class DashboardRepository:
    @staticmethod
    def monthly_totals(user, movement_type, start_date, ):
        return (
            CashMovement.objects.filter(
                user=user,
                type=movement_type,
                date__gte=start_date,
            )
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )