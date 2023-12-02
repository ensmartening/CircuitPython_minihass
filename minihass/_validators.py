"""Functions to validate various parameters passed to device and entity classes
"""

VALID_ENTITY_CATEGORIES = ["diagnostic", "config"]


def validate_entity_category(category: str) -> str:
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


def validate_string(param, none_ok: bool = False) -> str | type(None):
    """Validates that the entry is a non-null string. If `none_ok` is set to `True`,
        then `None` values are also accepted.

    Args:
        param (str): Parameter to validate
        none_ok (bool, optional): True if `None` is a valid parameter, defaults to
            `False`

    Raises:
        TypeError : On a type that is not `str`, unless `none_ok` is `True`
        ValueError : On a null string

    Returns:
        Validated parameter
    """
    if param == None:
        if not none_ok:
            raise TypeError("String expected, got None")

    elif isinstance(param, (str)):
        if param == "" and not none_ok:
            raise ValueError("Null string not allowed")

    else:
        raise TypeError(f"String expected, got {type(param).__name__}")

    return param if param else None


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
