from django.db.models import Q, Sum
from .models import CashEntry


class CashEntryRepository:

    def list_all(self):
        return CashEntry.objects.all()

    def create(self, data: dict) -> CashEntry:
        return CashEntry.objects.create(**data)

    def get_by_id(self, entry_id: int) -> CashEntry:
        return CashEntry.objects.get(pk=entry_id)

    def delete(self, entry: CashEntry) -> None:
        entry.delete()

    def get_summary(self) -> dict:
        qs = CashEntry.objects.aggregate(
            total_in=Sum('amount', filter=Q(type=CashEntry.EntryType.IN)),
            total_out=Sum('amount', filter=Q(type=CashEntry.EntryType.OUT)),
        )
        total_in = qs['total_in'] or 0
        total_out = qs['total_out'] or 0
        return {
            'total_in': total_in,
            'total_out': total_out,
            'balance': total_in - total_out
        }
