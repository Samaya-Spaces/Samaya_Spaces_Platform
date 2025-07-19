from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.urls import reverse

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
    location_preference = models.CharField(max_length=255, blank=True, help_text="e.g., Downtown, near the university")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Roommate profile for {self.user.username}"
    def get_absolute_url(self):
        return reverse('roommates:detail', kwargs={'pk': self.pk})