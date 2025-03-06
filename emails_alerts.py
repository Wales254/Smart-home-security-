import smtplib

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USERNAME = 'your-email@gmail.com'  # Replace with your email
GMAIL_PASSWORD = 'your-app-password'  # Generate an app password

def send_email(subject, content, recipient="your-recipient@gmail.com"):
    try:
        headers = f"From: {GMAIL_USERNAME}\nSubject: {subject}\nTo: {recipient}\nMIME-Version: 1.0\nContent-Type: text/html"

        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.starttls()
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit()

        print("✅ Email Sent Successfully")
    except Exception as e:
        print(f"❌ Email Failed: {e}")

# Test Email Sending
if __name__ == "__main__":
    send_email("Test Alert", "This is a test email from Smart Home Security System.")
