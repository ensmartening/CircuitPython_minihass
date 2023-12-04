"""
Defines base classes for components that only publish shates (e.g. sensors),
as well as components that accept commands (e.g. switches)
"""
from __future__ import annotations
from . import _validators as validators
import microcontroller
import json
from os import getenv


class _Entity(object):
    """Parent class for child classes representing Home Assistant entities. Cannot be
    instantiated directly.

    Args:
        name (int, optional) : Entity Name. Can be null if only the device name is
            relevant. One of ``name`` or ``object_id`` must be set.
        device_class (str, optional) : `Device class <https://www.home-assistant.io/integrations/binary_sensor/#device-class>`_
            of the entity. Defaults to :class:`None`
        entity_category (str, optional) : Set to specify `DIAGNOSTIC` or `CONFIG`
            entities.
        object_id (str, optional) : Set to generate ``entity_id`` from ``object_id``
            instead of ``name``. One of ``name`` or ``object_id`` must be set.
        icon (str, optional) : Send update events even when the state hasn't changed,
            defaults to :class:`False`
        enabled_by_default (bool, optional) : Defines the number of seconds after the
            sensor's state expires, if it's not updated. After expiry, the sensor's
            state becomes unavailable. Defaults to :class:`False`.
    """

    COMPONENT = None

    if hasattr(microcontroller, "cpu"):
        _chip_id = f"{int.from_bytes(microcontroller.cpu.uid, 'big'):x}"
    else:
        _chip_id = "1337d00d"  # for testing

    def __init__(self,
        name: str = None,
        entity_category: str = None,
        device_class: str = None,
        object_id: str = None,
        icon: str = None,
        enabled_by_default: bool = True,):

        if self.__class__ == _Entity:
            raise RuntimeError("Entity class cannot be raised on its own")

        self.name = validators.validate_string(name, none_ok=True)

        self.entity_category = validators.validate_entity_category(entity_category)

        self.device_class = validators.validate_string(device_class, none_ok=True)

        if object_id:
            self.object_id = f"{validators.validate_id_string(object_id)}{_Entity._chip_id}"
        elif name:
            self.object_id = f"{validators.validate_id_string(name)}{_Entity._chip_id}"
        else:
            raise ValueError("One of name or object_id must be set")


        self.icon = validators.validate_string(icon, none_ok=True)

        self.enabled_by_default = validators.validate_bool(enabled_by_default)

        self._availability = False

        self.component_config = {}

    @property
    def availability(self) -> bool:
        """Availability of the entity. Setting this property triggers :meth:`publish_availability()`."""
        return self._availability

    @availability.setter
    def availability(self, value: str):
        self._availability = validators.validate_bool(value)
        # self.publish_availability()

    def announce(self, device: "Device") -> bool:  # type: ignore (forward declaration)
        """Send MQTT discovery message for this entity only.

        Args:
            device (Device) : Parent device of this entity

        Returns:
            bool: :class:`True` if successful.
        """

        discovery_topic = f"{device.mqtt_discovery_prefix}/{self.COMPONENT}/{device.device_id}/{self.object_id}/config"
        print(discovery_topic)
        discovery_payload = {
            "avty": [
                {"t": f"{self.COMPONENT}/{self.object_id}/availability"},
                {"t": f"device/{device.device_id}/availability"},
            ],
            "dev": {
                "mf": device.manufacturer,
                "hw": device.hw_version,
                "ids": [device.device_id],
                "cns": device.connections,
            },
            "dev_cla": self.device_class,
            "en": self.enabled_by_default,
            "ent_cat": self.entity_category,
            "ic": self.icon,
            "name": self.name,
            "stat_t": f"device/{device.device_id}/state",
            "val_tpl": f"{{{{ value_json.{self.object_id}}}}}",
        }

        discovery_payload.update(self.component_config)

        print(json.dumps(discovery_payload))

        return True

    def publish_availability(self) -> bool:
        """Explicitly publishes availability of the entity.

        This function is called automatically when :attr:`availability` property is
        changed.

        Returns:
            bool : :class:`True` if successful.
        """
        # TODO: Implement availability updates
        raise NotImplementedError

        return True


# class _CommandEntity(_Entity):
#     """Parent class representing a Home Assistant Entity that accepts commands"""

#     pass
