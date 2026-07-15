from datetime import date, timedelta

from django.db.models import Sum
from django.utils import timezone

from apps.cash.repositories import CashMovementRepository

from .repositories import DashboardRepository


def _first_day_months_ago(reference: date, months_back: int) -> date:
    year = reference.year
    month = reference.month - months_back
    while month <= 0:
        month += 12
        year -= 1
    return date(year, month, 1)


def _last_12_month_keys(reference: date) -> list[date]:
    return [_first_day_months_ago(reference, i) for i in range(11, -1, -1)]


class DashboardService:
    @staticmethod
    def monthly_series(user, movement_type: str):
        today = timezone.localdate()
        start_date = _first_day_months_ago(today, 11)

        rows = DashboardRepository.monthly_totals(user, movement_type, start_date)
        totals_by_month = {row["month"]: row["total"] for row in rows}

        return [
            {
                "month": month_start.strftime("%m/%y"),
                "value": totals_by_month.get(month_start, 0),
            }
            for month_start in _last_12_month_keys(today)
        ]
    
    @staticmethod
    def period_summary(user):
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        def totals(date_from, date_to):
            qs = CashMovementRepository.list_history(user, date_from=date_from, date_to=date_to)
            income = qs.filter(type="income").aggregate(total=Sum("amount"))["total"] or 0
            expense = qs.filter(type="expense").aggregate(total=Sum("amount"))["total"] or 0
            return {"income": income, "expense": expense}
        
        return {
            "today": totals(today, today),
            "week": totals(week_start, today),
            "month": totals(month_start, today),
        }
        