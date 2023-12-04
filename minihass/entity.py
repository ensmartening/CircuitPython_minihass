"""
Defines base classes for components that only publish shates (e.g. sensors),
as well as components that accept commands (e.g. switches)
"""
from __future__ import annotations
from . import _validators as validators
import microcontroller
import json
from os import getenv


class Entity(object):
    """Parent class for child classes representing Home Assistant entities. Cannot be
    instantiated directly.

    Args:
        name (int, optional) : Entity Name. Can be null if only the device name is
            relevant. One of ``name`` or ``object_id`` must be set.
        device_class (str, optional) : Device class of the entity. Defaults to
            :class:`None`
        entity_category (str, optional) : Set to specify `DIAGNOSTIC` or `CONFIG`
            entities.
        object_id (str, optional) : Set to generate ``entity_id`` from ``object_id``
            instead of ``name``. One of ``name`` or ``object_id`` must be set.
        unique_id_suffix (str, optional) : The entity's ``unique_id`` is genrated by
            concatenating ``name`` or ``object_id`` onto the device's unique
            identifier. Set to use a different string, or if ``name`` and ``object_id``
            are both :class:`None`
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

    def __new__(cls, *args, **kwargs):
        if cls is Entity:  # Prevent instantiation of the base class
            raise TypeError(f"only children of '{cls.__name__}' may be instantiated")
        return object.__new__(cls)

    def __init__(self, **kwargs):

        self.name = (
            validators.validate_string(kwargs["name"], none_ok=True)
            if "name" in kwargs
            else None
        )

        self.category = (
            validators.validate_entity_category(kwargs["category"])
            if "category" in kwargs
            else None
        )

        self.device_class = (
            validators.validate_string(kwargs["device_class"], none_ok=True)
            if "device_class" in kwargs
            else None
        )

        if kwargs["object_id"]:
            self.object_id = (
                f"{validators.validate_id_string(kwargs['object_id'])}{Entity._chip_id}"
            )
        elif kwargs["name"]:
            self.object_id = (
                f"{validators.validate_id_string(kwargs['name'])}{Entity._chip_id}"
            )
        else:
            raise ValueError("One of name or object_id must be set")

        self.unique_id_prefix = (
            validators.validate_string(kwargs["unique_id"], none_ok=True)
            if "unique_id" in kwargs
            else None
        )

        self.icon = (
            validators.validate_string(kwargs["icon"], none_ok=True)
            if "icon" in kwargs
            else None
        )

        self.enabled_by_default = (
            validators.validate_bool(kwargs["enabled_by_default"])
            if "enabled_by_default" in kwargs
            else True
        )

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
            "ent_cat": self.category,
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


class _CommandEntity(Entity):
    """Parent class representing a Home Assistant Entity that accepts commands"""

    pass
