from validate_b import is_valid_email


def test_accepts_normal_address():
    assert is_valid_email("first.last@example.com") is True


def test_rejects_address_without_dot():
    assert is_valid_email("user@example") is False


def test_rejects_300_character_address():
    address = "a" * 288 + "@example.com"

    assert len(address) == 300
    assert is_valid_email(address) is False


def test_rejects_non_string_address():
    assert is_valid_email(None) is False