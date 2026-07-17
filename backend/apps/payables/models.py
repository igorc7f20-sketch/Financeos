from django.conf import settings
from django.db import models


class Payable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payables")
    description = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    installments_count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class PayableInstallment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        PAID = "paid", "Pago"

    payable = models.ForeignKey(Payable, on_delete=models.CASACADE, related_name="installments")
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField(db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["due_date"]