from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from core.exceptions import ServiceException

from .models import CashMovement
from .repositories import (
    CashBalanceRepository,
    CashClosingRepository,
    CashMovementRepository,
)


class CashService:
    @staticmethod
    def status(user):
        balance = CashBalanceRepository.get_or_create(user)
        today = timezone.localdate()
        income, expense = CashMovementRepository.totals_for_date(user, today)

        return {
            "current_balance": balance.current_balance,
            "today_income": income,
            "today_expense": expense,
            "today_balance": Decimal(income) - Decimal(expense),
            "date": today,
        }

    @staticmethod
    def today_movements(user):
        today = timezone.localdate()
        return CashMovementRepository.list_history(user, date_from=today, date_to=today)
    
    @staticmethod
    def history(user, filters: dict):
        today = timezone.localdate()
        date_from = filters.get("date_from") or today.replace(day=1)
        date_to = filters.get("date_to") or today

        if date_from > date_to:
            raise ServiceException("A data inicial não pode ser posterior à data final.")
        
        return CashMovementRepository.list_history(user, date_from+date_from, date_to=date_to)

    @staticmethod
    @transaction.atomic
    def create_movement(user, data):
        amount = Decimal(str(data["amount"]))

        if amount <= 0:
            raise ServiceException("Amount must be greater than zero.")

        movement_type = data["type"]
        balance = CashBalanceRepository.get_or_create(user)

        if movement_type == CashMovement.MovementType.INCOME:
            balance.current_balance += amount

        elif movement_type == CashMovement.MovementType.EXPENSE:
            balance.current_balance -= amount

        else:
            raise ServiceException("Invalid movement type.")

        balance.save()

        return CashMovementRepository.create(
            user=user,
            type=movement_type,
            description=data["description"],
            amount=amount,
            date=timezone.localdate(),
        )

    @staticmethod
    @transaction.atomic
    def close_today(user):
        today = timezone.localdate()

        if CashClosingRepository.exists_for_date(user, today):
            raise ServiceException("Cash already closed for today.")

        balance = CashBalanceRepository.get_or_create(user)
        income, expense = CashMovementRepository.totals_for_date(user, today)

        closing = CashClosingRepository.create(
            user=user,
            date=today,
            opening_balance=balance.current_balance
            - Decimal(income)
            + Decimal(expense),
            total_income=income,
            total_expense=expense,
            closing_balance=balance.current_balance,
        )

        CashMovementRepository.archive_for_date(user, today)

        return closing
