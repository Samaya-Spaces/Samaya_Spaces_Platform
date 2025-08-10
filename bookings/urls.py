
from django.urls import path
from . import views

# This creates the 'bookings' namespace.
app_name = 'bookings'

urlpatterns = [
    # The name here is now 'create', which matches the template.
    path('request/<int:listing_id>/', views.create_booking_request, name='create'),
    
    path('update/<int:booking_id>/<str:new_status>/', views.update_booking_status, name='update_status'),
]