import django_filters

from transaction.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    # start_date = django_filters.DateFilter(field_name="created_at", lookup_expr="gt")
    # end_date = django_filters.DateFilter(field_name="created_at", lookup_expr="lt")

    class Meta:
        model = Transaction
        fields = ("from_wallet", "to_wallet")
