from rest_framework.routers import SimpleRouter

from transaction.api.views import TransactionViewSet

router = SimpleRouter()
router.register(r"wallets", TransactionViewSet, basename="transaction")

urlpatterns = [] + router.urls
