
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation



@login_required
def inbox_view(request):
    """
    Displays a list of all conversations for the logged-in user.
    """
    # Get all conversation objects where the current user is a participant
    conversations = request.user.conversations.all().order_by('-created_at')
    
    return render(request, 'chats/inbox.html', {
        'conversations': conversations
    })
@login_required
def chat_room_view(request, conversation_id):
    # Get the conversation object.
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    
    # --- Security Check ---
    # Ensure the logged-in user is actually a participant in this conversation.
    if request.user not in conversation.participants.all():
        # You can create a simple 'unauthorized.html' template
        # or redirect them to the homepage with an error message.
        return render(request, 'unauthorized.html', status=403)
        
    # Render the chat room template, passing the conversation object.
    return render(request, 'chats/room.html', {
        'conversation': conversation
    })