"""Implements the binary_sensor MQTT component"""
from .entity import _Entity as Entity
from . import _validators as validators


class BinarySensor(Entity):
    """
    Class representing a Home Assistant Binary Sensor entity.

    Args:
        name (int, optional) : Entity Name. Can be null if only the device name is
            relevant.
        entity_category (str, optional) : Set to specify `DIAGNOSTIC` or `CONFIG`
            entities.
        device_class (str, optional) : `Device class <https://www.home-assistant.io/integrations/binary_sensor/#device-class>`_
            of the entity. Defaults to :class:`None`
        object_id (str, optional) : Set to generate ``entity_id`` from ``object_id``
            instead of ``name``.
        icon (str, optional) : Send update events even when the state hasn't changed,
            defaults to :class:`False`.
        enabled_by_default (bool, optional) : Defines the number of seconds after the
            sensor's state expires, if it's not updated. After expiry, the sensor's
            state becomes unavailable. Defaults to :class:`False`.
        force_update  (bool, optional) : Specifies whether the entity should be enabled
            when it is first added, defaults to :class:`False`.
        expire_after (bool, optional) : Defines the number of seconds after the
            sensor's state expires, if it's not updated. After expiry, the sensor's
            state becomes unavailable. Defaults to :class:`False`.
    """

    COMPONENT = "binary_sensor"

    def __init__(
        self,
        name: str = None,
        entity_category: str = None,
        device_class: str = None,
        object_id: str = None,
        icon: str = None,
        enabled_by_default: bool = True,
        # Component-specific arguments start here
        force_update: bool = False,
        expire_after: int = None,
    ):

        super().__init__(
            name=name,
            entity_category=entity_category,
            device_class=device_class,
            object_id=object_id,
            icon=icon,
            enabled_by_default=enabled_by_default,
        )

        self.expire_after = validators.validate_bool(expire_after)
        self.force_update = validators.validate_bool(force_update)

        self.component_config = {
            "expire_after": self.expire_after,
            "force_update": self.force_update,
        }
