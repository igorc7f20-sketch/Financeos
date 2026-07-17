from .models import Payable, PayableInstallment


class PayblabeRepository:
    @staticmethod
    def create_payable(user, description, total_amount, installments_count):
        return Payable.objects.create(
            user=user,
            description=description,
            total_amount=total_amount,
            installments_count=installments_count,
        )
    
    @staticmethod
    def bulk_create_installments(installments):
        return PayableInstallment.objects.bulk_create(installments)
    

class PayableInstallmentRepository:
    @staticmethod
    def list(user, status=None, date_from=None, date_to=None):
        qs = PayableInstallment.objects.filter(payable__user=user).select_related("payable")
        if status:
            qs = qs.filter(status=status)
        if date_from:
            qs = qs.filter(due_date__gte=date_from)
        if date_to:
            qs = qs.filter(due_date__lte=date_to)
        return qs.order_by("due_date")
    
    @staticmethod
    def get(user, installment_id):
        return PayableInstallment.objects.select_related("payable").get(
            id=installment_id, payable__user=user
        )