from django.urls import path
from .views import CashStatusView, CashMovementListCreateView, CashCloseView

urlpatterns = [
    path("status/", CashStatusView.as_view(), name="cash-status"),
    path("movements/", CashMovementListCreateView.as_view(), name="cash-movement-list-create"),
    path("close/", CashCloseView.as_view(), name="cash-close"),
]