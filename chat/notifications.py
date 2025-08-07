# chat/notifications.py

import os
from twilio.rest import Client
from django.conf import settings

def send_sms_notification(to_phone_number, body):
    """
    Sends an SMS notification using Twilio.
    """
    # First, check if Twilio settings are configured to avoid errors
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

    if not all([account_sid, auth_token, twilio_number]):
        print("Twilio settings are not fully configured. SMS not sent.")
        return

    # Twilio trial accounts require you to verify the phone number you're sending TO.
    # Make sure the 'to_phone_number' has been verified in your Twilio console.
    
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=twilio_number,
            to=to_phone_number
        )
        print(f"SMS sent successfully to {to_phone_number}! SID: {message.sid}")
    except Exception as e:
        # Catch any exceptions from the Twilio API and print them
        print(f"Error sending SMS to {to_phone_number}: {e}")