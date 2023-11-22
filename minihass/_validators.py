"""Functions to validate various parameters passed to device and entity classes
"""

VALID_ENTITY_CATEGORIES = ["diagnostic", "config"]


def validate_entity_category(category: str): -> bool
    """Validates that the entity category is an allowed value

    :param category: Entity category to validate
    :type category: str
    :raises ValueError: The entity category is not valid
    """
    if category not in VALID_ENTITY_CATEGORIES:
        raise ValueError(
            f"Invalid entity category \"{category}\", must be one of ({'|'.join(VALID_ENTITY_CATEGORIES)})"
        )

    return True
