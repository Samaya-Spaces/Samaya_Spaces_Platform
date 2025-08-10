# listings/views.py

from django.shortcuts import render
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
from .filters import ListingFilter #<-- IMPORT THE NEW FILTER
from roommates.models import RoommateProfile # Import for the dashboard view

# --- MODIFIED LIST VIEW ---
class ListingListView(ListView):
    """
    Displays a list of all listings, with filtering capabilities.
    """
    model = Listing
    template_name = 'listings/listing_list.html'
    context_object_name = 'listings'
    paginate_by = 10 # Optional: adds pagination to show 10 listings per page

    def get_queryset(self):
        """
        Overrides the default queryset to apply filters from the URL.
        """
        queryset = super().get_queryset().order_by('-created_at')
        # self.filterset will be used in get_context_data
        self.filterset = ListingFilter(self.request.GET, queryset=queryset)
        # Return the filtered queryset for the template
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """
        Adds the filter form to the context so it can be rendered in the template.
        """
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

# --- OTHER LISTING VIEWS (Unchanged but included for completeness) ---

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'

    def test_func(self):
        listing = self.get_object()
        return self.request.user == listing.owner

class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    template_name = 'listings/listing_confirm_delete.html'
    success_url = reverse_lazy('listings:list')

    def test_func(self):
        listing = self.get_object()
        return self.request.user == listing.owner

class OwnerDashboardView(LoginRequiredMixin, ListView):
    model = Listing
    template_name = 'listings/dashboard.html'
    context_object_name = 'listings'

    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = self.request.user.roommate_profile
            context['roommate_requests'] = profile.requests_received.all().order_by('-created_at')
        except RoommateProfile.DoesNotExist:
            context['roommate_requests'] = None
        return context