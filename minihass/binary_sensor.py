"""Implements the binary_sensor MQTT component"""
from .entity import Entity
from . import _validators as validators


class BinarySensor(Entity):
    """
    Class representing a Home Assistant Binary Sensor entity.

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
        expire_after (bool, optional) : Defines the number of seconds after the
            sensor's state expires, if it's not updated. After expiry, the sensor's
            state becomes unavailable. Defaults to :class:`False`.
    """

    def __init__(
        self,
        name: str = None,
        category: str = None,
        object_id: str = None,
        unique_id_prefix: str = None,
        icon: str = None,
        force_update: bool = False,
        enabled_by_default: bool = False,
        expire_after: int = None,
    ):

        super().__init__(
            name=name,
            category=category,
            object_id=object_id,
            unique_id_prefix=unique_id_prefix,
            icon=icon,
            force_update=force_update,
            enabled_by_default=enabled_by_default,
        )

        self.expire_after = validators.validate_bool(expire_after)
