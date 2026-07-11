from django.conf import settings
from django.db import models


class CashBalance(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cash_balance",
    )
    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cash_balance"


class CashMovement(models.Model):
    class MovementType(models.TextChoices):
        INCOME = "income", "Income"
        EXPENSE = "expense", "Expense"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cash_movements",
    )
    type = models.CharField(max_length=10, choices=MovementType.choices)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cash_movement"
        ordering = ["-date", "-created_at"]


class CashClosing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cash_closings",
    )
    date = models.DateField()
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2)
    total_income = models.DecimalField(max_digits=12, decimal_places=2)
    total_expense = models.DecimalField(max_digits=12, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=12, decimal_places=2)
    closed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cash_closing"
        unique_together = ("user", "date")
        ordering = ["-date"]