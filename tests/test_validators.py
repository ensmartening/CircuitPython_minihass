import pytest
import minihass._validators as validators


def test_entity_validator():
    with pytest.raises(ValueError):
        o = validators.validate_entity_category("invalid")  # invalid value
    with pytest.raises(TypeError):
        o = validators.validate_entity_category(1)  # invalid type
    assert validators.validate_entity_category("config")  # valid option
