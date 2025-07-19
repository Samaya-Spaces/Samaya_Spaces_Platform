from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        # Add 'main_photo' to the list of fields
        fields = ['title', 'description', 'price_per_month', 'main_photo']