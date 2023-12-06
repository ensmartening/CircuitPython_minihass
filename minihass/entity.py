"""
Defines base classes for components that only publish shates (e.g. sensors),
as well as components that accept commands (e.g. switches)
"""
from __future__ import annotations

import json
from os import getenv

import microcontroller
from adafruit_minimqtt.adafruit_minimqtt import MQTT

from . import _validators as validators


class Entity(object):
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
        mqtt_client (adafruit_minimqtt.adafruit_minimqtt.MQTT, optional) : MMQTT object for
            communicating with Home Assistant. If the entity is a member of a device,
            the device's broker will be used instead.
    """

    COMPONENT = None

    @classmethod
    def chip_id(cls):
        try:
            _chip_id = f"{int.from_bytes(microcontroller.cpu.uid, 'big'):x}"
        except AttributeError:
            _chip_id = getenv("CPU_UID")
            if not _chip_id:
                raise RuntimeError(
                    "Can't get cpu.uid from microcontroller, and CPU_UID environment variable is not defined."
                )
        return _chip_id

    def __init__(
        self,
        name: str | None = None,
        entity_category: str | None = None,
        device_class: str | None = None,
        object_id: str | None = None,
        icon: str | None = None,
        enabled_by_default: bool = True,
        mqtt_client: MQTT | None = None,
    ):

        if self.__class__ == Entity:
            raise RuntimeError("Entity class cannot be raised on its own")

        self.name = validators.validate_string(name, none_ok=True)

        self.entity_category = validators.validate_entity_category(entity_category)

        self.device_class = validators.validate_string(device_class, none_ok=True)

        if object_id:
            self.object_id = (
                f"{validators.validate_id_string(object_id)}{Entity.chip_id()}"
            )
        elif name:
            self.object_id = f"{validators.validate_id_string(name)}{Entity.chip_id()}"
        else:
            raise ValueError("One of name or object_id must be set")

        self.icon = validators.validate_string(icon, none_ok=True)

        self.enabled_by_default = validators.validate_bool(enabled_by_default)

        self.mqtt_client = mqtt_client

        self._availability = False
        self.component_config = {}
        self.device: "Device" | None = None  # type: ignore

    @property
    def availability(self) -> bool:
        """Availability of the entity. Setting this property triggers :meth:`publish_availability()`."""
        return self._availability

    @availability.setter
    def availability(self, value: bool):
        self._availability = validators.validate_bool(value)
        # self.publish_availability()

    def announce(self):
        """Send MQTT discovery message for this entity only.

        Raises:
            ValueError : If the entity or its parent device does not have a valid
                ``mqtt_client`` set.
            RuntimeError : If the MQTT client is not connected
        """

        if self.device:
            self.mqtt_client = self.device.mqtt_client

        if not isinstance(self.mqtt_client, MQTT):
            raise ValueError("mqtt_client not set")

        elif not self.mqtt_client.is_connected():
            raise RuntimeError("mqtt_client not connected")

        if self.device:
            discovery_topic = f"homeassistant/{self.COMPONENT}/{self.device.device_id}/{self.object_id}/config"
            state_topic = self.device.state_topic
        else:
            discovery_topic = f"homeassistant/{self.COMPONENT}/{self.object_id}/config"
            state_topic = f"entity/{self.object_id}/state"

        print(discovery_topic)
        discovery_payload = {
            "avty": [{"t": f"{self.COMPONENT}/{self.object_id}/availability"}],
            "dev_cla": self.device_class,
            "en": self.enabled_by_default,
            "ent_cat": self.entity_category,
            "ic": self.icon,
            "name": self.name,
            "stat_t": state_topic,
            "val_tpl": f"{{{{ value_json.{self.object_id} }}}}",
        }

        if self.device:
            discovery_payload.update(self.device.device_config)
            discovery_payload["avty"].append({"t": self.device.availability_topic})

        if self.component_config:
            discovery_payload.update(self.component_config)

        print(json.dumps(discovery_payload))

        self.mqtt_client.publish(
            discovery_topic, json.dumps(discovery_payload), True, 1
        )

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


# class _CommandEntity(Entity):
#     """Parent class representing a Home Assistant Entity that accepts commands"""

#     pass
