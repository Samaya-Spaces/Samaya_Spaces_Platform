# bookings/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # This is the line that defines the name 'create_booking'
    path('request/<int:listing_id>/', views.create_booking_request, name='create_booking'),
    
    path('update/<int:booking_id>/<str:new_status>/', views.update_booking_status, name='update_booking_status'),
]