from rest_framework import serializers


class MonthlyPointSerializer(serializers.Serializer):
    month = serializers.CharField()
    value = serializers.DecimalField(max_digits=12, decimal_places=2)


class PeriodTotalsSerializer(serializers.Serializer):
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expense = serializers.DecimalField(max_digits=12, decimal_places=2)


class PeriodSummarySerializer(serializers.Serializer):
    today = PeriodTotalsSerializer()
    week = PeriodTotalsSerializer()
    month = PeriodTotalsSerializer()
