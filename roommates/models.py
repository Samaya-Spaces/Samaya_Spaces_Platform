# roommates/models.py

from django.db import models
from django.conf import settings
from django.urls import reverse
import requests 

class RoommateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='roommate_profile'
    )
    bio = models.TextField(blank=True, help_text="A bit about yourself, your lifestyle, and what you're looking for.")
    budget = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Your estimated monthly budget for rent."
    )
    preferred_move_in_date = models.DateField(null=True, blank=True)
    

    location = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="e.g., Downtown, near the university"
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # --------------------------------

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Roommate profile for {self.user.username}"

    def get_absolute_url(self):
        return reverse('roommates:detail', kwargs={'pk': self.pk})

    # Add the SAME save method as in the Listing model
    def save(self, *args, **kwargs):
        if self.location and (not self.latitude or not self.longitude):
            try:
                url = 'https://nominatim.openstreetmap.org/search'
                params = {'q': self.location, 'format': 'json', 'limit': 1}
                headers = {'User-Agent': 'SamayaSpaces/1.0'}
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                if data:
                    self.latitude = data[0].get('lat')
                    self.longitude = data[0].get('lon')
            except requests.exceptions.RequestException as e:
                print(f"Geocoding failed for roommate profile: {e}")
        
        super().save(*args, **kwargs)
class RoommateRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
    ]

    profile = models.ForeignKey(
        RoommateProfile,
        on_delete=models.CASCADE,
        related_name='requests_received'
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requests_sent'
    )
    message = models.TextField(help_text="Introduce yourself and explain why you'd be a good roommate.")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.requester.username} to {self.profile.user.username}"