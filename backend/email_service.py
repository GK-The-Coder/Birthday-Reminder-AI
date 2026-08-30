import json
import os
import smtplib
from email.mime.text import MIMEText
from urllib import error, request


def _send_via_resend(receiver, subject, body):
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("EMAIL_FROM", "WishMate <noreply@resend.dev>")

    if not api_key:
        raise RuntimeError("RESEND_API_KEY must be configured when EMAIL_PROVIDER=resend")

    payload = json.dumps({
        "from": from_email,
        "to": [receiver],
        "subject": subject,
        "html": body,
    }).encode("utf-8")

    req = request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=20) as response:
            response.read()
        return
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Resend email failed: {details}") from exc


def send_email(receiver, subject, body):
    provider = os.getenv("EMAIL_PROVIDER", "smtp").lower()

    if provider == "resend":
        _send_via_resend(receiver, subject, body)
        return

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