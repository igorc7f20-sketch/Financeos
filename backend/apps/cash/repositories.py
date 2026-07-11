from django.db.models import Sum
from django.utils import timezone

from .models import CashBalance, CashClosing, CashMovement


class CashBalanceRepository:
    @staticmethod
    def get_or_create(user):
        balance, _ = CashBalance.objects.get_or_create(user=user)
        return balance


class CashMovementRepository:
    @staticmethod
    def list_today(user):
        today = timezone.localdate()
        return CashMovement.objects.filter(
            user=user,
            date=today,
            is_archived=False,
        )

    @staticmethod
    def list_history(user, date_from=None, date_to=None):
        qs = CashMovement.objects.filter(user=user)

        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs

    @staticmethod
    def create(user, **data):
        return CashMovement.objects.create(user=user, **data)

    @staticmethod
    def totals_for_date(user, date):
        qs = CashMovement.objects.filter(user=user, date=date)

        income = qs.filter(type="income").aggregate(total=Sum("amount"))["total"] or 0

        expense = qs.filter(type="expense").aggregate(total=Sum("amount"))["total"] or 0

        return income, expense

    @staticmethod
    def archive_for_date(user, date):
        return CashMovement.objects.filter(
            user=user,
            date=date,
            is_archived=False,
        ).update(
            is_archived=True,
            archived_at=timezone.now(),
        )


class CashClosingRepository:
    @staticmethod
    def exists_for_date(user, date):
        return CashClosing.objects.filter(user=user, date=date).exists()

    @staticmethod
    def create(user, **data):
        return CashClosing.objects.create(user=user, **data)
