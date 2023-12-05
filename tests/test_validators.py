import pytest

import minihass._validators as validators


def test_validate_entity_category():
    with pytest.raises(ValueError):
        o = validators.validate_entity_category("invalid")  # invalid value
    with pytest.raises(TypeError):
        o = validators.validate_entity_category(1)  # invalid type
    assert validators.validate_entity_category("config") == "config"  # valid option


def test_validate_string():
    with pytest.raises(TypeError):
        o = validators.validate_string(1, strict=True)  # invalid type, integer
    assert validators.validate_string(1) == "1"  # Non-strict
    with pytest.raises(TypeError):
        o = validators.validate_string(None)  # invalid type, None not allowed
    with pytest.raises(ValueError):
        o = validators.validate_string("")  # invalid type, Null string not allowed
    assert validators.validate_string(None, none_ok=True) == None  # valid type
    assert validators.validate_string("foo") == "foo"  # valid string
    assert validators.validate_string("", none_ok=True) == None  # Null string is None


def test_validate_hostname():
    with pytest.raises(TypeError):
        o = validators.validate_hostname_string(1)  # Invalid type
    for h in ["foo$bar", "-foobar", "foobar-"]:
        with pytest.raises(ValueError):
            o = validators.validate_hostname_string(
                h, strict=True
            )  # Invalid characters
    for h, r in [
        ("foo bar# $ #baz", "foo-bar-baz"),
        ("foo-bar123", "foo-bar123"),
        ("-foobar", "foobar"),
        ("f", "f"),
    ]:
        assert validators.validate_hostname_string(h) == r  # Normalized hostnames
    with pytest.raises(ValueError):
        o = validators.validate_hostname_string("# $")  # Un-normalizable hostname


def test_validate_id():
    with pytest.raises(TypeError):
        o = validators.validate_id_string(1)  # Invalid type
    for i in ["foo$bar", "_foobar", "foobar_", "fooBar"]:
        with pytest.raises(ValueError):
            o = validators.validate_id_string(i, strict=True)  # Invalid characters
    for i, r in [
        ("foo bar# $ #baz", "foo_bar_baz"),
        ("foobar", "foobar"),
        ("_foobar", "foobar"),
        ("fooBAR", "foobar"),
        ("f", "f"),
    ]:
        assert validators.validate_id_string(i) == r  # Normalized ids
    with pytest.raises(ValueError):
        o = validators.validate_id_string("# $")  # Un-normalizable id


def test_validate_bool():
    with pytest.raises(TypeError):
        o = validators.validate_bool(1, True)  # invalid type
    assert validators.validate_bool(0) == False  # falsy value
    assert validators.validate_bool(1) == True  # truthy value
    assert validators.validate_bool(True) == True  # valid bool
    assert validators.validate_bool(False) == False  # valid bool
    assert validators.validate_bool(None) == False  # None is False
