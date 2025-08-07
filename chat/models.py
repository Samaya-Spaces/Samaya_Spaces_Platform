# chat/models.py
from django.db import models
from django.conf import settings

class Conversation(models.Model):
    """Represents a chat conversation between two or more users."""
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # A helpful representation, e.g., "Conversation between userA, userB"
        participant_names = ", ".join([user.username for user in self.participants.all()])
        return f"Conversation between {participant_names}"

class Message(models.Model):
    """Represents a single message within a conversation."""
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure messages are always ordered by when they were created
        ordering = ['timestamp']

    def __str__(self):
        return f"Message by {self.author.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"