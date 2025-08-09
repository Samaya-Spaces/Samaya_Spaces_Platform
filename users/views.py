from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Use the correct name for our new homepage
            return redirect('listing_list') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

