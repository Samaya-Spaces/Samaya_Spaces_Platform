# roommates/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from .models import RoommateProfile, RoommateRequest
from .forms import RoommateProfileForm, RoommateRequestForm
from .filters import RoommateProfileFilter #<-- IMPORT THE NEW FILTER

# --- MODIFIED LIST VIEW ---
class RoommateProfileListView(ListView):
    """
    Displays a list of all roommate profiles, with filtering capabilities.
    """
    model = RoommateProfile
    template_name = 'roommates/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 10

    def get_queryset(self):
        """
        Overrides the default queryset to apply filters from the URL.
        """
        queryset = super().get_queryset().order_by('-created_at')
        self.filterset = RoommateProfileFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """
        Adds the filter form to the context.
        """
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

# --- OTHER ROOMMATE VIEWS (Unchanged but included for completeness) ---

class RoommateProfileDetailView(FormMixin, DetailView):
    model = RoommateProfile
    template_name = 'roommates/profile_detail.html'
    form_class = RoommateRequestForm

    def get_success_url(self):
        return reverse('roommates:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user != self.object.user:
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        existing_request = RoommateRequest.objects.filter(profile=self.object, requester=self.request.user, status='PENDING').exists()
        if existing_request:
            messages.info(self.request, "You already have a pending request for this person.")
        else:
            req = form.save(commit=False)
            req.profile = self.object
            req.requester = self.request.user
            req.save()
            messages.success(self.request, "Your connection request has been sent!")
        return super().form_valid(form)

class RoommateProfileCreateView(LoginRequiredMixin, CreateView):
    model = RoommateProfile
    form_class = RoommateProfileForm
    template_name = 'roommates/profile_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RoommateProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RoommateProfile
    form_class = RoommateProfileForm
    template_name = 'roommates/profile_form.html'
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

@login_required
def my_profile_view(request):
    try:
        profile = request.user.roommate_profile
        return redirect('roommates:detail', pk=profile.pk)
    except RoommateProfile.DoesNotExist:
        return redirect('roommates:create')

@login_required
def update_request_status(request, request_id, new_status):
    req = get_object_or_404(RoommateRequest, pk=request_id)
    if request.user != req.profile.user:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('listings:owner_dashboard')
    if request.method == 'POST':
        if new_status.upper() in ['APPROVED', 'DENIED']:
            req.status = new_status.upper()
            req.save()
            messages.success(request, f"Request has been {new_status.lower()}.")
        else:
            messages.error(request, "Invalid status.")
        return redirect('listings:owner_dashboard')
    return redirect('listings:owner_dashboard')