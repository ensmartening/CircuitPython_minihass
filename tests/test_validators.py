import pytest

import minihass._validators as validators


def test_validate_entity_category_valueerror():
    with pytest.raises(ValueError):
        validators.validate_entity_category("invalid")  # invalid value


def test_validate_entity_category_typeerror():
    with pytest.raises(TypeError):
        validators.validate_entity_category(1)  # type: ignore invalid type


@pytest.mark.parametrize("n", ["config", "diagnostic", None])
def test_validate_entity_category_valid(n):
    assert validators.validate_entity_category("config") == "config"  # valid option


def test_validate_string_typeerror():
    with pytest.raises(TypeError):
        validators.validate_string(1, strict=True)  # invalid type, integer
    with pytest.raises(TypeError):
        validators.validate_string(None)  # invalid type, None not allowed


def test_validate_string_valueerror():
    with pytest.raises(ValueError):
        validators.validate_string("")  # invalid type, Null string not allowed


@pytest.mark.parametrize("n, x", [(1, "1"), ("foo", "foo"), (None, ""), ("", "")])
def test_validate_string_normalized(n, x):
    assert validators.validate_string(n, null_ok=True) == x


def test_validate_hostname_string_typeerror():
    with pytest.raises(TypeError):
        validators.validate_hostname_string(1)  # type: ignore invalid type


@pytest.mark.parametrize("n", ["foo$bar", "-foobar", "foobar-"])
def test_validate_hostname_string_valueerror(n):
    with pytest.raises(ValueError):
        validators.validate_hostname_string(n, strict=True)


@pytest.mark.parametrize(
    "n, x",
    [
        ("foo bar# $ #baz", "foo-bar-baz"),
        ("foo-bar123", "foo-bar123"),
        ("-foobar", "foobar"),
        ("f", "f"),
    ],
)
def test_validate_hostname_string_normalized(n, x):
    assert validators.validate_hostname_string(n) == x  # Normalized hostnames


def test_validate_hostname_string_normalize_failure():
    with pytest.raises(ValueError):
        o = validators.validate_hostname_string("# $")  # Un-normalizable hostname


def test_validate_id_string_typeerror():
    with pytest.raises(TypeError):
        o = validators.validate_id_string(1)  # type: ignore


@pytest.mark.parametrize("n", ["foo$bar", "_foobar", "foobar_", "fooBar"])
def test_validate_id_string_valueerror(n):
    with pytest.raises(ValueError):
        validators.validate_id_string(n, strict=True)  # Invalid characters


@pytest.mark.parametrize(
    "n, x",
    [
        ("foo bar# $ #baz", "foo_bar_baz"),
        ("foobar", "foobar"),
        ("_foobar", "foobar"),
        ("fooBAR", "foobar"),
        ("f", "f"),
    ],
)
def test_validate_id_string_normalized(n, x):
    assert validators.validate_id_string(n) == x  # Normalized ids


def test_validate_id_string_normalize_failure():
    with pytest.raises(ValueError):
        validators.validate_id_string("# $")  # Un-normalizable id


def test_validate_bool_typeerror():
    with pytest.raises(TypeError):
        validators.validate_bool(1, True)  # invalid type


@pytest.mark.parametrize(
    "n, x", [(True, True), (0, False), (1, True), ("foo", True), ("", False)]
)
def test_validate_bool_normalized(n, x):
    assert validators.validate_bool(n) == x


@pytest.mark.parametrize(
    "n, x",
    [
        ("yes", "yes"),
        ("no", "no"),
        ("always", "always"),
        (True, "yes"),
        ("", "no"),
        ("ALWAYS", "always"),
    ],
)
def test_validate_queue_option(n, x):
    assert validators.validate_queue_option(n, strict=False) == x


def test_validate_queue_option_strict():
    with pytest.raises(ValueError):
        validators.validate_queue_option("foo", strict=True)
