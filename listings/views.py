
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
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile


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
    
#PDF generation view
def rental_agreement_pdf(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    # Example static values (replace later with real form data)
    tenant_name = "John Doe"
    start_date = "2025-08-15"
    end_date = "2026-08-15"

    # Render HTML template with context
    html_string = render_to_string('listings/rental_agreement.html', {
        'listing': listing,
        'tenant_name': tenant_name,
        'start_date': start_date,
        'end_date': end_date,
    })

    # Generate PDF
    with tempfile.NamedTemporaryFile(delete=True) as output:
        HTML(string=html_string).write_pdf(output.name)
        output.seek(0)
        pdf_content = output.read()

    # Return PDF as download
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rental_agreement_{listing_id}.pdf"'
    return response