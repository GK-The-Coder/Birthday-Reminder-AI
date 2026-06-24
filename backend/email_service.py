import os
import smtplib
from email.mime.text import MIMEText

def send_email(receiver, subject, body):

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    )

    server.login(sender, password)

    server.sendmail(
        sender,
        receiver,
        msg.as_string()
    )

    server.quit()