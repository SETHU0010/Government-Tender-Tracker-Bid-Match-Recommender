import smtplib
from email.mime.text import MIMEText
from config import GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT, GMAIL_SENDER_EMAIL, GMAIL_PASSWORD

def send_email_notification(recipient_email, subject, body):
    try:
        server = smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT)
        server.starttls() # Secure the connection
        server.login(GMAIL_SENDER_EMAIL, GMAIL_PASSWORD) # Consider using OAuth2

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_SENDER_EMAIL
        msg['To'] = recipient_email

        server.sendmail(GMAIL_SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    send_email_notification("sethumadhavanvelu2002@gmail.com", "New Tender Alert!", "A new tender matching your profile has been found.")