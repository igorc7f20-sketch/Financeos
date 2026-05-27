from rest_framework import serializers
from .models import CashEntry


class CashEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CashEntry
        fields = ['id', 'type', 'amount', 'description', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor deve ser maior que zero.")
        return value
    

class CashSummarySerializer(serializers.Serializer):
    total_in = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_out = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)