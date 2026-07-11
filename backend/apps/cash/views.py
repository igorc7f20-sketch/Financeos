"""
Cash Views - API Layer.

Handles HTTP request/response only.
All logic delegated to the service layer.
"""

from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from core.exceptions import ServiceException
from core.pagination import StandardResultsPagination
from .serializers import (
    CashStatusSerializer,
    CashMovementSerializer,
    CashMovementInputSerializer,
    CashHistoryFilterSerializer,
)
from .services import CashService


class CashStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: CashStatusSerializer},
        summary="Get current cash status",
        tags=["Cash"],
    )
    def get(self, request):
        data = CashService.status(request.user)
        return Response(CashStatusSerializer(data).data)


class CashMovementListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("date_from", str, description="Filter from date (DD-MM-YYYY)"),
            OpenApiParameter("date_to", str, description="Filter to date (DD-MM-YYYY)"),
        ],
        responses={200: CashMovementSerializer(many=True)},
        summary="List cash movement history with period filter",
        tags=["Cash"],
    )
    def get(self, request):
        filter_serializer = CashHistoryFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        try:
            movements = CashService.history(request.user, filter_serializer.validated_data)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)

        totals = CashService.history_totals(movements)

        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(movements, request)
        response = paginator.get_paginated_response(
            CashMovementSerializer(page, many=True).data
        )

        normalized_totals = {}
        for key, value in totals.items():
            if isinstance(value, Decimal):
                normalized_totals[key] = str(value.quantize(Decimal("0.01")))
            elif isinstance(value, (int, float)):
                normalized_totals[key] = f"{float(value):.2f}"
            else:
                normalized_totals[key] = value
        response.data["totals"] = normalized_totals
        return response
    
    @extend_schema(
        request=CashMovementInputSerializer,
        responses={201: CashMovementSerializer},
        summary="Create a new cash movement",
        tags=["Cash"],
    )
    def post(self, request):
        serializer = CashMovementInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            movement = CashService.create_movement(request.user, serializer.validated_data)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(
            CashMovementSerializer(movement).data,
            status=status.HTTP_201_CREATED,
        )
    

class CashCloseView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Close cash for today", tags=["Cash"])
    def post(self, request):
        try:
            CashService.close_today(request.user)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(status=status.HTTP_204_NO_CONTENT)