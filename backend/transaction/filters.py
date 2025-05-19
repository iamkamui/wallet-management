import django_filters
from django.db.models import Q, QuerySet

from transaction.models import Transaction, Wallet


class TransactionFilter(django_filters.FilterSet):
    wallet = django_filters.CharFilter(method="filter_wallet_transactions")
    start_date = django_filters.DateFilter(field_name="created_at", lookup_expr="gt")
    end_date = django_filters.DateFilter(field_name="created_at", lookup_expr="lt")

    def filter_wallet_transactions(
        self, queryset: QuerySet[Transaction], name: str, value: Wallet
    ) -> QuerySet[Transaction]:
        filter = queryset.filter(Q(from_wallet__number=value) | Q(to_wallet__number=value))
        return filter

    class Meta:
        model = Transaction
        fields = ()
