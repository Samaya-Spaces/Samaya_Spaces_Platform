from django import forms
from .models import RoommateProfile

class RoommateProfileForm(forms.ModelForm):
    class Meta:
        model = RoommateProfile
        fields = ['bio', 'budget', 'preferred_move_in_date', 'location_preference']
        widgets = {
            'preferred_move_in_date': forms.DateInput(attrs={'type': 'date'}),
        }