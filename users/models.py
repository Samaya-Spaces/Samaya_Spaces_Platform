# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # We could add extra fields here in the future, for example:
    # bio = models.TextField(blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    phone_number = models.CharField(max_length=15, blank=True, help_text="Enter phone number in format: +9779847352926")
    pass