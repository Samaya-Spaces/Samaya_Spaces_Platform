# listings/models.py

from django.db import models
from django.conf import settings
from django.urls import reverse
import requests  # For making API calls to geocode

class Listing(models.Model):
    # --- Core Fields ---
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2)

    # --- Photo Field ---
    main_photo = models.ImageField(
        upload_to='listings/', 
        blank=True, 
        null=True,
        help_text="The main photo for the listing."
    )

    # --- Location & Map Fields ---
    location = models.CharField(
        max_length=255, 
        blank = True,
        null = True,
        help_text="E.g., 'Bijuli Bazar Near Kings College, 'Shakhamul' or 'UN Park'"
    )
    latitude = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Automatically generated from the location. Do not edit."
    )
    longitude = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Automatically generated from the location. Do not edit."
    )

    # --- Timestamps (Defined only ONCE) ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # --- Methods ---

    def __str__(self):
        """A human-readable representation of the listing object."""
        return self.title

    def get_absolute_url(self):
        """Returns the canonical URL for a listing's detail page."""
        return reverse('listings:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        A custom save method to automatically geocode the location
        into latitude and longitude coordinates before saving.
        """
        # Check if the location has been set and if coordinates are missing.
        # This prevents making an API call every single time the model is saved.
        if self.location and (not self.latitude or not self.longitude):
            try:
                # Use the Nominatim API from OpenStreetMap for geocoding
                url = 'https://nominatim.openstreetmap.org/search'
                params = {'q': self.location, 'format': 'json', 'limit': 1}
                headers = {'User-Agent': 'SamayaSpaces/1.0 (your-email@example.com)'} # It's good practice to identify your app
                
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
                
                data = response.json()
                if data:
                    # If we got a result, update the latitude and longitude fields
                    self.latitude = data[0].get('lat')
                    self.longitude = data[0].get('lon')
            
            except requests.exceptions.RequestException as e:
                # If the API call fails for any reason (network error, timeout, etc.),
                # print an error to the console but don't crash the application.
                print(f"Error: Geocoding request failed for location '{self.location}'. Reason: {e}")
        
        # Finally, call the original, real save method from the parent class
        super().save(*args, **kwargs)