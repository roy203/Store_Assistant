import pytest

from store_assistant.agent.utils import normalize_phone, validate_phone


@pytest.mark.parametrize(
    "phone",
    [
        "(555) 555-5555",
        "555-555-5555",
        "5555555555",
        "+15555555555",
        "555.555.5555",
        "1-555-555-5555",
    ],
)
def test_valid_phones(phone):
    assert validate_phone(phone) is True


@pytest.mark.parametrize(
    "phone",
    [
        "123",
        "abcdefghij",
        "12345678901234",
        "",
        "555-55-555",
        "55555555",
        None,
    ],
)
def test_invalid_phones(phone):
    assert validate_phone(phone) is False


def test_normalize_strips_formatting():
    assert normalize_phone("(555) 555-5555") == "5555555555"


def test_normalize_strips_dashes():
    assert normalize_phone("555-555-5555") == "5555555555"


def test_normalize_strips_dots():
    assert normalize_phone("555.555.5555") == "5555555555"


def test_normalize_strips_country_code():
    assert normalize_phone("+15555555555") == "5555555555"


def test_normalize_plain_10_digits():
    assert normalize_phone("5555555555") == "5555555555"


def test_validate_and_normalize_consistent():
    valid_phones = [
        "(555) 555-5555",
        "555-555-5555",
        "5555555555",
        "+15555555555",
        "555.555.5555",
    ]
    for phone in valid_phones:
        assert validate_phone(phone) is True
        assert len(normalize_phone(phone)) == 10
