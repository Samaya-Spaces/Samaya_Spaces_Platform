# listings/urls.py

from django.urls import path
from .import views
from .views import (
    ListingListView,
    ListingDetailView,
    ListingCreateView,
    ListingUpdateView,
    ListingDeleteView,
    OwnerDashboardView,
)

# This line is CRITICAL. It creates the 'listings' namespace.
# Without this, {% url 'listings:list' %} will fail.
app_name = 'listings'

# This is the "phonebook" for the listings app.
urlpatterns = [
    # This line connects the empty path ('') to the ListView 
    # and gives it the name 'list'.
    # This is the definition for 'listings:list'.
    path('', ListingListView.as_view(), name='list'),

    # The rest of the URLs for this app
    path('dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('new/', ListingCreateView.as_view(), name='create'),
    path('<int:pk>/', ListingDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ListingUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ListingDeleteView.as_view(), name='delete'),
     path(
        "agreements/<int:listing_id>/rental.pdf",
        views.rental_agreement_pdf,
        name="rental_agreement_pdf",
    ),
]