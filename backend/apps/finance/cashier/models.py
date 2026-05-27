from django.db import models


class CashEntry(models.Model):
    class EntryType(models.TextChoices):
        IN = "in", "Entrada"
        OUT = "out", "Saída"

    type = models.CharField(max_length=3, choices=EntryType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(max_length=255, blank=True, default="")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.get_type_display()} - R$ {self.amount} ({self.date})"