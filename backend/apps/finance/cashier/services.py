from .repositories import CashEntryRepository
from .models import CashEntry


class CashEntryService:
    def __init__(self):
        self.repo = CashEntryRepository()

    def list_entries(self):
        return self.repo.list_all()
    
    def create_entry(self, data: dict) -> CashEntry:
        if data.get("amount", 0) <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return self.repo.create(data)
    
    def delete_entry(self, entry_id: int) -> None:
        entry = self.repo.get_by_id(entry_id)
        self.repo.delete(entry)

    def get_summary(self) -> dict:
        return self.repo.get_summary()