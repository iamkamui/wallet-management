from rest_framework.routers import SimpleRouter

from transaction.api.views import TransactionViewSet

router = SimpleRouter()
router.register(r"transaction", TransactionViewSet, basename="wallet")

urlpatterns = [] + router.urls
