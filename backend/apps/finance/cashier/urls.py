from rest_framework.routers import DefaultRouter
from .views import CashEntryViewSet

router = DefaultRouter()
router.register(r'cashier', CashEntryViewSet, basename='cashier')

urlpatterns = router.urls
