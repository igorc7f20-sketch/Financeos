from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from core.exceptions import ServiceException
from core.pagination import StandardResultsPagination

from .serializers import (
    PayableInputSerializer, PayableInstallmentSerializer,
    PayableFilterSerializer, PayableSummarySerializer,
)
from .services import PayableService


class PayableListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("status", str, description="pending | paid"),
            OpenApiParameter("date_from", str),
            OpenApiParameter("date_to", str),
        ],
        responses={200: PayableInstallmentSerializer(many=True)},
        tags=["Payables"],
    )
    def get(self, request):
        filter_serializer = PayableFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        installments = PayableService.list_installments(request.user, filter_serializer.validated_data)

        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(installments, request)
        return paginator.get_paginated_response(
            PayableInstallmentSerializer(page, many=True).data
        )

    @extend_schema(request=PayableInputSerializer, responses={201: PayableInstallmentSerializer(many=True)}, tags=["Payables"])
    def post(self, request):
        serializer = PayableInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            payable = PayableService.create_payable(request.user, **serializer.validated_data)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(
            PayableInstallmentSerializer(payable.installments.all(), many=True).data,
            status=status.HTTP_201_CREATED,
        )


class PayableInstallmentPayView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: PayableInstallmentSerializer}, tags=["Payables"])
    def post(self, request, installment_id):
        try:
            installment = PayableService.mark_as_paid(request.user, installment_id)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(PayableInstallmentSerializer(installment).data)


class PayableSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: PayableSummarySerializer}, tags=["Payables"])
    def get(self, request):
        return Response(PayableSummarySerializer(PayableService.summary(request.user)).data)