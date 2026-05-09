"""
Transaction Views — API Layer.

Handles HTTP request/response only.
All logic delegated to the service layer.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from core.exceptions import ServiceException
from core.pagination import StandardResultsPagination
from .serializers import (
    CategorySerializer,
    CategoryInputSerializer,
    TransactionSerializer,
    TransactionInputSerializer,
    TransactionFilterSerializer,
)
from .services import CategoryService, TransactionService


# ─── Category Views ───────────────────────────────────────────────────────────


class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        summary="List user categories",
        tags=["Categories"],
    )
    def get(self, request):
        categories = CategoryService.list(request.user)
        return Response(CategorySerializer(categories, many=True).data)

    @extend_schema(
        request=CategoryInputSerializer,
        responses={201: CategorySerializer},
        summary="Create a category",
        tags=["Categories"],
    )
    def post(self, request):
        serializer = CategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            category = CategoryService.create(request.user, **serializer.validated_data)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(
            CategorySerializer(category).data, status=status.HTTP_201_CREATED
        )


class CategoryDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Delete a category",
        tags=["Categories"],
    )
    def delete(self, request, pk):
        try:
            CategoryService.delete(request.user, pk)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Transaction Views ────────────────────────────────────────────────────────


class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "type", str, description="Filter by type: income or expense"
            ),
            OpenApiParameter("category_id", int, description="Filter by category ID"),
            OpenApiParameter(
                "date_from", str, description="Filter from date (YYYY-MM-DD)"
            ),
            OpenApiParameter("date_to", str, description="Filter to date (YYYY-MM-DD)"),
            OpenApiParameter("search", str, description="Search by title"),
        ],
        responses={200: TransactionSerializer(many=True)},
        summary="List transactions with filters",
        tags=["Transactions"],
    )
    def get(self, request):
        filter_serializer = TransactionFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        transactions = TransactionService.list(
            request.user, filter_serializer.validated_data
        )

        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(transactions, request)
        return paginator.get_paginated_response(
            TransactionSerializer(page, many=True).data
        )

    @extend_schema(
        request=TransactionInputSerializer,
        responses={201: TransactionSerializer},
        summary="Create a transaction",
        tags=["Transactions"],
    )
    def post(self, request):
        serializer = TransactionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            transaction = TransactionService.create(
                request.user, serializer.validated_data
            )
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(
            TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED
        )


class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: TransactionSerializer},
        summary="Get a transaction",
        tags=["Transactions"],
    )
    def get(self, request, pk):
        try:
            transaction = TransactionService.get(request.user, pk)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(TransactionSerializer(transaction).data)

    @extend_schema(
        request=TransactionInputSerializer,
        responses={200: TransactionSerializer},
        summary="Update a transaction",
        tags=["Transactions"],
    )
    def put(self, request, pk):
        serializer = TransactionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            transaction = TransactionService.update(
                request.user, pk, serializer.validated_data
            )
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(TransactionSerializer(transaction).data)

    @extend_schema(
        summary="Delete a transaction",
        tags=["Transactions"],
    )
    def delete(self, request, pk):
        try:
            TransactionService.delete(request.user, pk)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        return Response(status=status.HTTP_204_NO_CONTENT)
