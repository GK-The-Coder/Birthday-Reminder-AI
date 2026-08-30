from types import SimpleNamespace

from app import build_signup_options, get_frontend_base_url, get_registration_status


def test_registration_requires_confirmation_when_session_missing():
    result = get_registration_status(
        SimpleNamespace(
            user=SimpleNamespace(id="user-123"),
            session=None,
        )
    )

    assert result["requires_email_confirmation"] is True
    assert "confirm your account" in result["message"].lower()


def test_signup_redirect_points_to_configured_frontend_url(monkeypatch):
    monkeypatch.setenv("FRONTEND_URL", "https://wish-mate.vercel.app")
    monkeypatch.delenv("APP_URL", raising=False)
    monkeypatch.delenv("SITE_URL", raising=False)

    assert get_frontend_base_url() == "https://wish-mate.vercel.app"
    assert build_signup_options("Alice")["email_redirect_to"] == "https://wish-mate.vercel.app/login"
