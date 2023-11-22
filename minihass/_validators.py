"""Functions to validate various parameters passed to device and entity classes
"""

VALID_ENTITY_CATEGORIES = ["diagnostic", "config"]


def validate_entity_category(category: str):
    """Validates that the entity category is an allowed value

    :param category: Entity category to validate
    :type category: str
    :raises ValueError: _description_
    """
    if category not in VALID_ENTITY_CATEGORIES:
        raise ValueError("Invalid entity category")
