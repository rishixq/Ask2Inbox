import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


def send_email(to_email: str, subject: str, body: str):
    """
    Transport-only email sender.

    ❌ No formatting
    ❌ No mutation
    ❌ No templates

    Body MUST be LLM output passed as-is.
    """

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        raise ValueError("Email credentials not set")

    msg = MIMEText(body, "plain")
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
