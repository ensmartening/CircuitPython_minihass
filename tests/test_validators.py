import pytest
import minihass._validators as validators


def test_validate_entity_category():
    with pytest.raises(ValueError):
        o = validators.validate_entity_category("invalid")  # invalid value
    with pytest.raises(TypeError):
        o = validators.validate_entity_category(1)  # invalid type
    assert validators.validate_entity_category("config") == "config"  # valid option


def test_validate_string_or_none():
    with pytest.raises(TypeError):
        o = validators.validate_string_or_none(1)  # invalid type
    assert validators.validate_string_or_none(None) == None  # valid type
    assert validators.validate_string_or_none("foo") == "foo"  # valid string
    assert validators.validate_string_or_none("") == None  # Null string is None
