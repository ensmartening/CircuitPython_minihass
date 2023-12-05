"""Functions to validate various parameters passed to device and entity classes
"""

import re

VALID_ENTITY_CATEGORIES = ["diagnostic", "config"]


def validate_entity_category(category: str | None) -> str | None:
    """Validates that the entity category is an allowed value

    Args:
        category (str) : Entity category to validate

    Raises:
        ValueError : The entity category is not valid
    """

    if not isinstance(category, (str, type(None))):
        raise TypeError(f"String or None expected, got {type(category).__name__}")

    if category not in VALID_ENTITY_CATEGORIES + [None]:
        raise ValueError(
            f"Invalid entity category \"{category}\", must be one of ({'|'.join(VALID_ENTITY_CATEGORIES)})"
        )

    return category


def validate_string(param, strict: bool = False, none_ok: bool = False) -> str | None:
    """Validates that the entry is a non-null string. If `none_ok` is set to `True`,
        then `None` values are also accepted.

    Args:
        param (str):  Parameter to validate
        strict (bool) : When :class:`True`, return string representation of ``param``.
            When :class:`False`, raises an exception if ``param`` is not a string.
            Defaults to :class:`False`
        none_ok (bool, optional) : :class:`True` if `None` is a valid parameter.
            Defaults to :class:`False`

    Raises:
        TypeError : On a type that is not `str`, unless `none_ok` is `True`
        ValueError : On a null string

    Returns:
        Validated parameter
    """
    if param == None:
        if not none_ok:
            raise TypeError("String expected, got None")
        else:
            return None

    if not isinstance(param, str):
        if strict:
            raise TypeError(f"String expected, got {type(param).__name__}")
        else:
            param = str(param)
            print(param)

    if param == "":
        if none_ok:
            return None
        else:
            raise ValueError("Null string not allowed")

    return param


def validate_hostname_string(param: str, strict: bool = False) -> str:
    """Validates that the entry is a valid hostname.

    If ``strict`` is :class:`False`, a normalized hostname is returned by stripping
    non-alphanumeric characters and converting underscores or spaces to hyphens. If
    ``strict`` is :class:`True`, an invalid hostname raises an exception.

    Args:
        param (str) : Hostname to validate
        strict (bool) : When :class:`True`, disallow invalid hostnames. When
            :class:`False`, convert ``param`` to a valid hostname. Defaults to
            :class:`False`

    Returns:
        str: Normalized hostname

    Raises:
        ValueError : On an invalid hostname string when ``strict`` is :class:`True`, or
            when the input string cannot be normalized to a hostname
    """

    if not isinstance(param, str):
        raise TypeError(f"Expected str, got {type(param).__name__}")

    if not strict:
        param = re.sub(r"[^A-Za-z0-9-\ _]", "", param)  # Remove non-alphanumerics
        param = re.sub(r"[\ _]+", "-", param)  # Underscores and spaces to hyphens
        param = re.sub(r"^-|-$", "", param)  # First and last must be alphanumeric

    if not re.match(r"(?:^[A-Za-z0-9](?:$|(?:[A-Za-z0-9-]*[A-Za-z0-9]$)+))", param):
        if strict:
            raise ValueError("Invalid hostname")
        else:
            raise ValueError("Could not normalize string to valid hostname")

    return param


def validate_id_string(param: str, strict: bool = False) -> str:
    """Validates that the entry is a valid device or entity id.

    If ``strict`` is :class:`False`, a normalized id is returned by stripping
    non-alphanumeric characters, converting hyphens or spaces to underscores, and
    converting to lowercase. If ``strict`` is :class:`True`, an invalid id raises an
    exception.

    Args:
        param (str) : id to validate
        strict (bool) : When :class:`True`, disallow invalid ids. When
            :class:`False`, convert ``param`` to a valid id. Defaults to
            :class:`False`.

    Returns:
        str: Normalized id.

    Raises:
        ValueError : On an invalid id string when ``strict`` is :class:`True`, or
            when the input string cannot be normalized to a id.
    """

    if not isinstance(param, str):
        raise TypeError(f"Expected str, got {type(param).__name__}")

    if not strict:
        param = param.lower()  # Lowercase
        param = re.sub(r"[^a-z0-9-\ _]", "", param)  # Remove non-alphanumerics
        param = re.sub(r"[\ -]+", "_", param)  # Spaces and hyphens to underscores
        param = re.sub(r"^_|_$", "", param)  # First and last must be alphanumeric

    if not re.match(r"(?:^[a-z0-9](?:$|(?:[a-z0-9_]*[a-z0-9]$)+))", param):
        if strict:
            raise ValueError("Invalid id")
        else:
            raise ValueError("Could not normalize string to valid id")

    return param


def validate_bool(param, strict: bool = False) -> bool:
    """Validates that the entry is a :class:`bool`. :class:`None` is returned as
    :class:`False`.

    Args:
        param (bool) : Parameter to validate
        strict (bool, optional) : Disallow "truthy" or "falsy" values, defaults to
            :class:`False`

    Raises:
        TypeError: On a type that is not :class:`bool`, or :class:`None` if ``strict``
            is set to :class:`True`

    Returns:
        Validated parameter

    """
    if strict and not isinstance(param, (bool, type(None))):
        raise TypeError(f"Expected bool, got {type(param).__name__}")

    return True if param else False
