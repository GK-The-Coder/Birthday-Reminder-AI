import pytest
from pydantic import ValidationError

from models.birthday_model import Birthday


def test_birthday_accepts_valid_date_and_email():
    birthday = Birthday(
        name="Alex",
        email="alex@example.com",
        birthday="2024-02-29",
    )

    assert birthday.birthday.isoformat() == "2024-02-29"


@pytest.mark.parametrize("birthday", ["2023-02-29", "2024-13-01", "not-a-date"])
def test_birthday_rejects_invalid_dates(birthday):
    with pytest.raises(ValidationError):
        Birthday(name="Alex", email="alex@example.com", birthday=birthday)


def test_birthday_rejects_invalid_email():
    with pytest.raises(ValidationError):
        Birthday(name="Alex", email="not-an-email", birthday="2024-02-29")