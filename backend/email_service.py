import os
import smtplib
from email.mime.text import MIMEText

def send_email(receiver, subject, body):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))

    if not sender or not password:
        raise RuntimeError("EMAIL_ADDRESS and EMAIL_PASSWORD must be configured")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())