from django import forms
from .models import RoommateProfile, RoommateRequest # Import both models

class RoommateProfileForm(forms.ModelForm):
    """
    Form for creating and updating the main roommate profile.
    """
    class Meta:
        model = RoommateProfile
        fields = ['bio', 'budget', 'preferred_move_in_date', 'location']
        widgets = {
            'preferred_move_in_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'bio': "About Me",
            'budget': "My Monthly Budget ($)",
            'preferred_move_in_date': "Preferred Move-in Date",
            'location': "Preferred Location(s)"
        }

class RoommateRequestForm(forms.ModelForm):
    """
    Form for sending a connection request to another user.
    """
    class Meta:
        model = RoommateRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Introduce yourself and explain why you think you would be a good roommate...'
            }),
        }
        labels = {
            'message': "" # Hide the default label to make the form cleaner
        }