from django.urls import path
from .views import DashboardMonthlyIncomeView, DashboardMonthlyExpenseView, DashboardPeriodSummaryView

urlpatterns = [
    path("monthly-income/", DashboardMonthlyIncomeView.as_view(), name="dashboard-monthly-income"),
    path("monthly-expense/", DashboardMonthlyExpenseView.as_view(), name="dashboard-monthly-expense"),
    path("period-summary/", DashboardPeriodSummaryView.as_view(), name="dashboard-period-summary"),
]