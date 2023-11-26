"""Functions to validate various parameters passed to device and entity classes
"""

VALID_ENTITY_CATEGORIES = ["diagnostic", "config"]


def validate_entity_category(category: str) -> str:
    """Validates that the entity category is an allowed value

    :param category: Entity category to validate
    :type category: str
    :raises ValueError: The entity category is not valid
    """

    if not isinstance(category, str):
        raise TypeError

    if category not in VALID_ENTITY_CATEGORIES:
        raise ValueError(
            f"Invalid entity category \"{category}\", must be one of ({'|'.join(VALID_ENTITY_CATEGORIES)})"
        )

    return category


def validate_string(param, none_ok: bool = False) -> str | type(None):
    """Validates that the entry is a non-null string. If `none_ok` is set to `True`,
        then `None` values are also accepted.
    :param param: Parameter to validate
    :param none_ok: True if `None` is a valid parameter, defaults to `False`
    :raises TypeError: On a type that is not `str`, unless `none_ok` is `True`
    :raises ValueError: On a null string
    :return: Validated parameter
    :rtype: str | bool
    """
    if param == None:
        if not none_ok:
            raise TypeError

    elif isinstance(param, (str)):
        if param == "" and not none_ok:
            raise ValueError

    else:
        raise TypeError

    return param if param else None


def validate_bool(param) -> bool:
    '''Validates that the entry is a `bool`. `None` is returned as `False`.

    :param param: Parameter to validate
    :raises TypeError: On a type that is not `bool` or `None`
    :return: Validate parameter
    :rtype: bool
    '''
    if not isinstance(param, (bool, type(None))):
        raise TypeError

    return param if param else False
