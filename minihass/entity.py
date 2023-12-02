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
    :type enabled_by_default: bool, optional

    """

    def __init__(self, **kwargs):
        """Base entity class"""

        self.name = (
            validators.validate_string(kwargs["name"], True)
            if "name" in kwargs
            else None
        )

        self.category = (
            validators.validate_entity_category(kwargs["category"])
            if "category" in kwargs
            else None
        )

        self.object_id = (
            validators.validate_string(kwargs["object_id"], True)
            if "object_id" in kwargs
            else None
        )

        self.unique_id_prefix = (
            validators.validate_string(kwargs["unique_id"], True)
            if "unique_id" in kwargs
            else None
        )

        self.icon = (
            validators.validate_string(kwargs["icon"], True)
            if "icon" in kwargs
            else None
        )

        self.force_update = (
            validators.validate_bool(kwargs["force_update"])
            if "force_update" in kwargs
            else None
        )

        self._availability = (
            validators.validate_bool(kwargs["enabled_by_default"])
            if "enabled_by_default" in kwargs
            else False
        )

        self._availability = False

    @property
    def availability(self) -> bool:
        """Availability of the entity. Setting this property triggers :meth:`publish_availability()`"""
        return self._availability

    @availability.setter
    def availability(self, value: str):
        validators.validate_bool(value)
        self._availability = value
        self.publish_availability()

    def publish_availability(self):
        """Explicitly publishes availability of the entity."""
        # TODO: Implement availability updates
        pass


class _CommandEntity(_Entity):
    """Parent class representing a Home Assistant Entity that accepts commands"""

    pass
