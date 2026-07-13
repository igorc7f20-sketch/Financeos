from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .serializers import MonthlyPointSerializer, PeriodSummarySerializer
from .services import DashboardService


class DashboardMonthlyIncomeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: MonthlyPointSerializer(many=True)}, tags=["Dashboard"])
    def get(self, request):
        return Response(
            MonthlyPointSerializer(
                DashboardService.monthly_series(request.user, "income"), many=True
            ).data
        )
    

class DashboardMonthlyExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: MonthlyPointSerializer(many=True)}, tags=["Dashboard"])
    def get(self, request):
        return Response(
            MonthlyPointSerializer(
                DashboardService.monthly_series(request.user, "expense"), many=True
            ).data
        )
    

class DashboardPeriodSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: PeriodSummarySerializer}, tags=["Dashboard"])
    def get(self, request):
        return Response(
            PeriodSummarySerializer(DashboardService.period_summary(request.user)).data
        )