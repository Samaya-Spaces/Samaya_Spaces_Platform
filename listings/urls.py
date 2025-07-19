# listings/urls.py

from django.urls import path
from .views import (
    ListingListView,
    ListingDetailView,
    ListingCreateView,
    ListingUpdateView,
    ListingDeleteView,
    OwnerDashboardView,
)

urlpatterns = [
    path('', ListingListView.as_view(), name='listing_list'),
    path('dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('new/', ListingCreateView.as_view(), name='listing_create'),
    path('<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('<int:pk>/edit/', ListingUpdateView.as_view(), name='listing_update'),
    path('<int:pk>/delete/', ListingDeleteView.as_view(), name='listing_delete'),
]