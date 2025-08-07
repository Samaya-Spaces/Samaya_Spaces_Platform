# listings/filters.py
import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    # This creates a filter for price that is "less than or equal to" the given value.
    price_per_month__lte = django_filters.NumberFilter(field_name='price_per_month', lookup_expr='lte', label='Max Price Per Month')

    # This creates a text search filter that looks in both the title and description.
    # 'icontains' means case-insensitive contains.
    query = django_filters.CharFilter(method='universal_search', label="Search by Keyword")

    class Meta:
        model = Listing
        # These are the fields we will directly filter on (not needed for custom ones above)
        fields = []

    def universal_search(self, queryset, name, value):
        # A custom method to search across multiple fields
        from django.db.models import Q
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )