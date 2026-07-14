"""
Cash Serializers - Content Layer.

Input validation and output transformation only.
No business rules here.
"""

from rest_framework import serializers
from .models import CashMovement


class CashMovementInputSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=["income", "expense"])
    payment_method = serializers.ChoiceField(
        choices=CashMovement.PaymentMethod.choices,
        required=False,
        allow_null=True,
    )
    description = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = CashMovement
        fields = ["type", "payment_method", "description", "amount"]


class CashMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashMovement
        fields = ["id", "type", "payment_method", "description", "amount", "date", "is_archived", "created_at"]
        read_only_fields = fields


class CashHistoryFilterSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)


class CashStatusSerializer(serializers.Serializer):
    current_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    today_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    today_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    today_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    date = serializers.DateField()