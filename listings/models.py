# listings/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse

class Listing(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2)
    
    # ADD THIS NEW FIELD
    main_photo = models.ImageField(upload_to='listings/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Tell Django to look for the URL named 'detail'
        # specifically inside the 'listings' app namespace.
        return reverse('listings:detail', kwargs={'pk': self.pk})