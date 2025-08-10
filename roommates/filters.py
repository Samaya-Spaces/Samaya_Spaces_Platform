# roommates/filters.py
import django_filters
from .models import RoommateProfile

class RoommateProfileFilter(django_filters.FilterSet):
    budget__lte = django_filters.NumberFilter(field_name='budget', lookup_expr='lte', label='Max Budget')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains', label='Location contains')

    class Meta:
        model = RoommateProfile
        fields = ['budget__lte', 'location']