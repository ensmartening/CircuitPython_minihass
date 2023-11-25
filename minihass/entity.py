"""
Defines base classes for components that only publish shates (e.g. sensors),
as well as components that accept commands (e.g. switches)
"""
from . import _validators as validators


class _Entity:
    """Parent class representing a Home Assistant entity
    :param name: Entity Name. Can be null if only device name is relevant
    :type name: str, optional
    :param entity_category: Set to speficy `DIAGNOSTIC` or `CONFIG` entites
    :type entity_category: str, optional
    :param object_id: Set to generate `entity_id` from `object_id` instead of `name`
    :type object_id: str, optional
    :param unique_id_suffix: Entity `unique_id` is genrated by concatenating `name`
    or `object_id` onto the device's unique identifier. Set to use a different string
    or if `name` and `object_id` are both `None`
    :type unique_id_suffix: str, optional
    :param icon: Override the device domain default icon
    :type icon: str, optional
    :param force_update: Send update events even when the state hasn't changed, defaults to `false`
    :type force_update: bool, optional
    :param enabled_by_default: Specifies whether the entity should be enabled when it is first added, defaults to `false`

    """

    def __init__(self, **kwargs):
        """Base entity class"""

        self.name = (
            validators.validate_string_or_none(kwargs["name"])
            if "name" in kwargs
            else None
        )

        self.category = (
            validators.validate_entity_category(kwargs["category"])
            if "category" in kwargs
            else None
        )

    pass


class _CommandEntity(_Entity):
    """Parent class representing a Home Assistant Entity that accepts commands"""

    def __init__(self, **kwargs):
        """init summary

        :param name: foo
        :type name: bar
        """
        if "category" in kwargs:
            self.category = validators.validate_entity_category(kwargs["category"])

    pass
