"""
Defines base classes for components that only publish shates (e.g. sensors),
as well as components that accept commands (e.g. switches)
"""
from . import _validators as validators


class Entity(object):
    """Parent class representing a Home Assistant entity. Cannot be instantiated
    directly.

    Args:
        name (int, optional) : Entity Name. Can be null if only the device name is
            relevant.
        entity_category (str, optional) : Set to specify `DIAGNOSTIC` or `CONFIG`
            entities.
        object_id (str, optional) : Set to generate ``entity_id`` from ``object_id``
            instead of ``name``
        unique_id_suffix (str, optional) : The entity's ``unique_id`` is genrated by
            concatenating ``name`` or ``object_id`` onto the device's unique
            identifier. Set to use a different string, or if ``name`` and ``object_id``
            are both :class:`None`
        icon (str, optional) : Send update events even when the state hasn't changed,
            defaults to :class:`False`
        force_update  (bool, optional) : Specifies whether the entity should be enabled
            when it is first added, defaults to :class:`False`
        enabled_by_default (bool, optional) : Defines the number of seconds after the
            sensor's state expires, if it's not updated. After expiry, the sensor's
            state becomes unavailable. Defaults to :class:`False`.
    """

    def __new__(cls, *args, **kwargs):
        if cls is Entity:
            raise TypeError(f"only children of '{cls.__name__}' may be instantiated")
        return object.__new__(cls)

    def __init__(self, **kwargs):

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

    @property
    def availability(self) -> bool:
        """Availability of the entity. Setting this property triggers :meth:`publish_availability()`"""
        return self._availability

    @availability.setter
    def availability(self, value: str):
        self._availability = validators.validate_bool(value)
        self.publish_availability()

    def publish_availability(self) -> bool:
        """Explicitly publishes availability of the entity.

        Returns:
            bool : :class:`True` if publishing succeeds, :class:`False` otherwise."""
        # TODO: Implement availability updates
        return True


class _CommandEntity(Entity):
    """Parent class representing a Home Assistant Entity that accepts commands"""

    pass
