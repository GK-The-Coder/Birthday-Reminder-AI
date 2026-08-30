from unittest.mock import MagicMock, patch

import email_service


def test_smtp_provider_sends_expected_message(monkeypatch):
    monkeypatch.setenv("EMAIL_ADDRESS", "sender@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "app-password")
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "465")
    monkeypatch.setenv("SMTP_USE_SSL", "true")
    server = MagicMock()
    server.__enter__.return_value = server

    with patch.object(email_service.smtplib, "SMTP_SSL", return_value=server) as smtp:
        email_service.send_email(
            "alex@example.com",
            "Happy Birthday",
            "Have a great day!",
        )

    smtp.assert_called_once_with("smtp.example.com", 465, timeout=15)
    server.login.assert_called_once_with("sender@example.com", "app-password")
    server.sendmail.assert_called_once()
    server.__enter__.assert_called_once_with()
    server.__exit__.assert_called_once()


def test_smtp_starttls_provider_starts_tls(monkeypatch):
    monkeypatch.setenv("EMAIL_ADDRESS", "sender@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "app-password")
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USE_SSL", "false")
    server = MagicMock()
    server.__enter__.return_value = server

    with patch.object(email_service.smtplib, "SMTP", return_value=server) as smtp:
        email_service.send_email("alex@example.com", "Subject", "Body")

    smtp.assert_called_once_with("smtp.example.com", 587, timeout=15)
    server.starttls.assert_called_once_with()
    server.login.assert_called_once_with("sender@example.com", "app-password")


def test_resend_provider_sends_expected_request(monkeypatch):
    monkeypatch.setenv("EMAIL_PROVIDER", "resend")
    monkeypatch.setenv("RESEND_API_KEY", "test-key")
    monkeypatch.setenv("EMAIL_FROM", "WishMate <noreply@wishmate.app>")

    with patch.object(email_service, "_send_via_resend", return_value=None) as send_via_resend:
        email_service.send_email("alex@example.com", "Subject", "Body")

    send_via_resend.assert_called_once_with("alex@example.com", "Subject", "Body")


def test_smtp_credentials_are_required(monkeypatch):
    monkeypatch.delenv("EMAIL_ADDRESS", raising=False)
    monkeypatch.delenv("EMAIL_PASSWORD", raising=False)

    try:
        email_service.send_email("alex@example.com", "Subject", "Body")
    except RuntimeError as error:
        assert "EMAIL_ADDRESS" in str(error)
    else:
        raise AssertionError("Missing SMTP credentials were accepted")
