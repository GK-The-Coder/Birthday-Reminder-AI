from types import SimpleNamespace

from app import get_registration_status


def test_registration_requires_confirmation_when_session_missing():
    result = get_registration_status(
        SimpleNamespace(
            user=SimpleNamespace(id="user-123"),
            session=None,
        )
    )

    assert result["requires_email_confirmation"] is True
    assert "confirm your account" in result["message"].lower()
