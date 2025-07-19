# bookings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from listings.models import Listing

@login_required
def create_booking_request(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if listing.owner == request.user:
        messages.error(request, "You cannot book your own listing.")
        return redirect('listing_detail', pk=listing_id)

    existing_booking = Booking.objects.filter(listing=listing, requester=request.user, status='PENDING').exists()
    if existing_booking:
        messages.info(request, "You already have a pending request for this listing.")
        return redirect('listing_detail', pk=listing_id)

    if request.method == 'POST':
        Booking.objects.create(listing=listing, requester=request.user)
        messages.success(request, "Your booking request has been sent to the owner.")
        return redirect('listing_detail', pk=listing_id)

    return redirect('listing_detail', pk=listing_id)


@login_required
def update_booking_status(request, booking_id, new_status):
    booking = get_object_or_404(Booking, pk=booking_id)

    if request.user != booking.listing.owner:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('owner_dashboard')

    if request.method == 'POST':
        if new_status in ['APPROVED', 'DENIED']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking has been {new_status.lower()}.")
        else:
            messages.error(request, "Invalid status.")
        return redirect('owner_dashboard')

    return redirect('owner_dashboard')