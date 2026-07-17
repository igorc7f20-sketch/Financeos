from datetime import date
from decimal import Decimal, ROUND_DOWN
from calendar import monthrange

from django.db.models import Sum
from django.utils import timezone

from core.exceptions import ServiceException

from .models import PayableInstallment
from .repositories import PayableRepository, PayableInstallmentRepository


def _add_months(reference: date, months: int) -> date:
    month_index = reference.month - 1 + months
    year = reference.year + month_index // 12
    month = month_index % 12 + 1
    day = min(reference.day, monthrange(year, month)[1])
    return date(year, month, day)


def _split_amount(total: Decimal, count: int) -> list[Decimal]:
    base = (total / count).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    amounts = [base] * count
    amounts[-1] += total - (base * count)
    return amounts


class PayableService:
    @staticmethod
    def create_payable(user, description, total_amount, installments_count, first_due_date):
        if total_amount <= 0:
            raise ServiceException("O valor total deve ser maior que zero.")
        if installments_count < 1:
            raise ServiceException("A quantidade de parcelas deve ser ao menos 1.")

        payable = PayableRepository.create_payable(user, description, total_amount, installments_count)
        amounts = _split_amount(total_amount, installments_count)

        installments = [
            PayableInstallment(
                payable=payable,
                installment_number=i + 1,
                due_date=_add_months(first_due_date, i),
                amount=amounts[i],
            )
            for i in range(installments_count)
        ]
        PayableRepository.bulk_create_installments(installments)
        return payable

    @staticmethod
    def list_installments(user, filters: dict):
        return PayableInstallmentRepository.list(
            user,
            status=filters.get("status"),
            date_from=filters.get("date_from"),
            date_to=filters.get("date_to"),
        )

    @staticmethod
    def mark_as_paid(user, installment_id):
        installment = PayableInstallmentRepository.get(user, installment_id)
        if installment.status == PayableInstallment.Status.PAID:
            raise ServiceException("Esta parcela já está paga.")
        installment.status = PayableInstallment.Status.PAID
        installment.paid_at = timezone.localdate()
        installment.save()
        return installment

    @staticmethod
    def summary(user):
        today = timezone.localdate()
        pending = PayableInstallmentRepository.list(user, status=PayableInstallment.Status.PENDING)
        overdue = pending.filter(due_date__lt=today)
        this_month = pending.filter(due_date__year=today.year, due_date__month=today.month)

        return {
            "overdue_total": overdue.aggregate(t=Sum("amount"))["t"] or 0,
            "overdue_count": overdue.count(),
            "this_month_total": this_month.aggregate(t=Sum("amount"))["t"] or 0,
            "this_month_count": this_month.count(),
        }