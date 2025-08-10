from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import RoommateProfile
from .forms import RoommateProfileForm

class RoommateProfileListView(ListView):
    model = RoommateProfile
    template_name = 'roommates/profile_list.html'
    context_object_name = 'profiles'

class RoommateProfileDetailView(DetailView):
    model = RoommateProfile
    template_name = 'roommates/profile_detail.html'

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
        return redirect('profile_detail', pk=profile.pk)
    except RoommateProfile.DoesNotExist:
        return redirect('profile_create')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- Static pages (add at the very end, below your existing code) ---
from django.shortcuts import render

def help_view(request):
    return render(request, 'help.html')

def about_view(request):
    return render(request, 'about.html')
