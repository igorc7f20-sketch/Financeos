from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .services import CashEntryService
from .serializers import CashEntrySerializer, CashSummarySerializer


class CashEntryViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CashEntryService()

    def list(self, request):
        entries = self.service.list_entries()
        serializer = CashEntrySerializer(entries, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CashEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            entry = self.service.create_entry(serializer.validated_data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(CashEntrySerializer(entry).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            self.service.delete_entry(pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Entrada não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        data = self.service.get_summary()
        serializer = CashSummarySerializer(data)
        return Response(serializer.data)
