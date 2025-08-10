from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q # Import Q for complex queries
from .models import Booking
from listings.models import Listing
from chat.models import Conversation # Import the Conversation model

@login_required
def create_booking_request(request, listing_id):
    """
    Handles a user's request to book a listing.
    """
    listing = get_object_or_404(Listing, pk=listing_id)

    # Security: Prevent owner from booking their own listing.
    if listing.owner == request.user:
        messages.error(request, "You cannot book your own listing.")
        return redirect('listings:detail', pk=listing_id)

    # Prevent duplicate requests (pending or approved).
    existing_booking = Booking.objects.filter(
        listing=listing, 
        requester=request.user
    ).filter(
        Q(status='PENDING') | Q(status='APPROVED')
    ).exists()

    if existing_booking:
        messages.info(request, "You already have an active request for this listing.")
        return redirect('listings:detail', pk=listing_id)

    # This view should only handle POST requests.
    if request.method == 'POST':
        Booking.objects.create(listing=listing, requester=request.user)
        messages.success(request, "Your booking request has been sent to the owner.")
        return redirect('listings:detail', pk=listing_id)

    # If accessed via GET, just redirect back.
    return redirect('listings:detail', pk=listing_id)


@login_required
def update_booking_status(request, booking_id, new_status):
    """
    Allows a listing owner to 'APPROVE' or 'DENY' a booking request.
    If approved, it creates a chat conversation between the two users.
    """
    booking = get_object_or_404(Booking, pk=booking_id)

    # Security: Ensure the user changing the status is the listing owner.
    if request.user != booking.listing.owner:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('listings:owner_dashboard')

    # This view should only handle POST requests.
    if request.method == 'POST':
        if new_status.upper() in ['APPROVED', 'DENIED']:
            booking.status = new_status.upper()
            booking.save()

            # ===================================================================
            # CORE LOGIC FOR CREATING A CHAT CONVERSATION
            # ===================================================================
            if booking.status == 'APPROVED':
                # Define the two participants of the conversation
                owner = booking.listing.owner
                requester = booking.requester
                
                # Check if a conversation between these two users already exists
                # This is a robust way to find the exact conversation
                conversation = Conversation.objects.filter(
                    participants=owner
                ).filter(
                    participants=requester
                ).first()
                
                # If no conversation exists, create a new one
                if conversation is None:
                    conversation = Conversation.objects.create()
                    conversation.participants.add(owner, requester)
                
                messages.success(request, f"Booking has been approved! A chat has been started with {requester.username}.")
            # ===================================================================
            else: # If status is 'DENIED'
                messages.success(request, "Booking has been successfully denied.")
        
        else: # If the status provided in the URL is invalid
            messages.error(request, "Invalid status update.")
            
        return redirect('listings:owner_dashboard')

    # If accessed via GET, just redirect back.
    return redirect('listings:owner_dashboard')