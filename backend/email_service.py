import os
import smtplib
from email.mime.text import MIMEText


def send_email(receiver, subject, body):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_use_ssl = os.getenv("SMTP_USE_SSL", "true").lower() == "true"

    if not sender or not password:
        raise RuntimeError("EMAIL_ADDRESS and EMAIL_PASSWORD must be configured")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    smtp_client = smtplib.SMTP_SSL if smtp_use_ssl else smtplib.SMTP
    with smtp_client(smtp_host, smtp_port, timeout=15) as server:
        if not smtp_use_ssl:
            server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())