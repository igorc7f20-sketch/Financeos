from django.utils import timezone
from rest_framework import serializers

from .models import PayableInstallment


class PayableInputSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    installments_count = serializers.IntegerField(min_value=1, default=1)
    first_due_date = serializers.DateField()


class PayableInstallmentSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source="payable.description", read_only=True)
    total_installments = serializers.IntegerField(source="payable.installments_count", read_only=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = PayableInstallment
        fields = [
            "id", "description", "installment_number", "total_installments",
            "due_date", "amount", "status", "paid_at", "is_overdue",
        ]
        read_only_fields = fields

    def get_is_overdue(self, obj):
        return obj.status == PayableInstallment.Status.PENDING and obj.due_date < timezone.localdate()


class PayableFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["pending", "paid"], required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)


class PayableSummarySerializer(serializers.Serializer):
    overdue_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    overdue_count = serializers.IntegerField()
    this_month_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    this_month_count = serializers.IntegerField()