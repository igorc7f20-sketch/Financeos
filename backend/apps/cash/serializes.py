from rest_framework import serializers


class CashMovementSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["income", "expense"])
    description = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
