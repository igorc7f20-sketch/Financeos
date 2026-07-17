from django.urls import path
from .views import PayableListCreateView, PayableInstallmentPayView, PayableSummaryView

urlpatterns = [
    path("", PayableListCreateView.as_view(), name="payable-list-create"),
    path("summary/", PayableSummaryView.as_view(), name="payable-summary"),
    path("installments/<int:installment_id>/pay/", PayableInstallmentPayView.as_view(), name="payable-installment-pay"),
]