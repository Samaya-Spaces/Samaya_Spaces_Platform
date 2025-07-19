
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Listing
from .forms import ListingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader

class ListingListView(ListView):
    model = Listing
    template_name = 'listings/listing_list.html'
    context_object_name = 'listings'
    # listings/views.py

from django.views.generic import ListView
from .models import Listing

# ... other views...

class ListingListView(ListView):
    model = Listing
    template_name = 'listings/listing_list.html'
    context_object_name = 'listings'

    def get_queryset(self):
        # This is a special method that gets the list of items for the view.
        # Let's see what it finds.
        queryset = super().get_queryset()
        
        print("--- DEBUGGING ListingListView ---")
        print("Listings found in database:", queryset)
        print("Number of listings found:", queryset.count())
        print("---------------------------------")
        
        return queryset

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'

    def form_valid(self, form):
        # Set the owner of the listing to the currently logged-in user
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'

    def test_func(self):
        # Check if the current user is the owner of the listing
        listing = self.get_object()
        return self.request.user == listing.owner

class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    template_name = 'listings/listing_confirm_delete.html'
    success_url = reverse_lazy('listing_list') # Redirect to homepage on success

    def test_func(self):
        # Check if the current user is the owner of the listing
        listing = self.get_object()
        return self.request.user == listing.owner

class OwnerDashboardView(LoginRequiredMixin, ListView):
    model = Listing
    template_name = 'listings/dashboard.html'
    context_object_name = 'listings'

    def get_queryset(self):
        # Filter listings to only show those owned by the current user
        return Listing.objects.filter(owner=self.request.user).order_by('-created_at')