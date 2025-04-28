from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

def send_sms_notification(recipient_phone, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            to=recipient_phone,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        print(f"SMS sent with SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

if __name__ == '__main__':
    send_sms_notification("+919159299878", "Alert: New matching tender available!")