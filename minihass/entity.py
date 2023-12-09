"""
Defines base classes for components that only publish shates (e.g. sensors),
as well as components that accept commands (e.g. switches)
"""
from __future__ import annotations

from json import dumps
from logging import WARN, WARNING
from os import getenv
from xml.dom.minidom import Attr

import adafruit_logging as logging
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
        logger_name (str) : Name for the :class:`adafruit_logging.logger` used by this
            object. Defaults to ``'minihass'``.
    """

    COMPONENT = None

    @classmethod
    def chip_id(cls):
        try:
            _chip_id = (
                f"{int.from_bytes(microcontroller.cpu.uid, 'big'):x}"  # type: ignore
            )
        except AttributeError:
            _chip_id = getenv("CPU_UID")
            if not _chip_id:
                raise RuntimeError(
                    "Can't get cpu.uid from microcontroller, and CPU_UID environment variable is not defined."
                )
        return _chip_id

    def __init__(
        self,
        *args,
        name: str | None = None,
        entity_category: str | None = None,
        device_class: str | None = None,
        object_id: str | None = None,
        icon: str | None = None,
        enabled_by_default: bool = True,
        mqtt_client: MQTT | None = None,
        logger_name: str = "minimqtt",
        **kwargs,
    ):

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(getattr(logging, getenv("LOGLEVEL", ""), WARNING))

        if self.__class__ == Entity:
            self.logger.error(
                "Attepted instantiation of parent class, raising an exception..."
            )
            raise RuntimeError("Entity class cannot be raised on its own")

        self.name = validators.validate_string(name, none_ok=True)
        self.logger.debug(f"Entity name: self.name")

        self.entity_category = validators.validate_entity_category(entity_category)
        self.logger.debug(f"Entity category: {self.entity_category}")

        self.device_class = validators.validate_string(device_class, none_ok=True)
        self.logger.debug(f"Entity device_class: {self.device_class}")

        if object_id:
            self.object_id = (
                f"{validators.validate_id_string(object_id)}{Entity.chip_id()}"
            )
            self.logger.debug(
                f"Entity object_id: {self.object_id} (set by object_id parameter)"
            )
        elif name:
            self.object_id = f"{validators.validate_id_string(name)}{Entity.chip_id()}"
            self.logger.debug(
                f"Entity object_id: {self.object_id} (derived from name parameter)"
            )
        else:
            raise ValueError("One of name or object_id must be set")

        self.icon = validators.validate_string(icon, none_ok=True)
        self.logger.debug(f"Entity icon: {self.icon}")

        self.enabled_by_default = validators.validate_bool(enabled_by_default)
        self.logger.debug(
            f"Entity {'enabled' if self.enabled_by_default else 'disabled'} by default"
        )

        self._mqtt_client = mqtt_client
        try:
            self.logger.debug(f"Entity MQTT client: {self._mqtt_client.broker}")  # type: ignore
        except AttributeError:
            self.logger.debug(
                f"MQTT{' broker' if self._mqtt_client else '_client'} not set"
            )

        self._availability = False

        self.device: "Device" | None = None  # type: ignore
        self.availability_topic = f"{self.COMPONENT}/{self.object_id}/availability"
        try:
            self.component_config
        except AttributeError:
            self.component_config = {}

        self.logger.info(f"Initialized {self.COMPONENT} {self.name}: {self.object_id} ")

        super().__init__(*args, **kwargs)

    @property
    def mqtt_client(self) -> MQTT:
        """Sets or gets the MQTT client for this entity. If this entity is a member
        of a device, the device MQTT client will be returned."""
        if self.device:
            return self.device.mqtt_client
        else:
            return self._mqtt_client  # type: ignore

    @mqtt_client.setter
    def mqtt_client(self, client: MQTT):
        self._mqtt_client = client
        self.logger.info(f"Entity MQTT client set")

    @property
    def availability(self) -> bool:
        """Availability of the entity. Setting this entity to :class:`false` makes the
        entity appear as `unavailable` in Home Assistant. This may be desired if, for
        instance, the sensor providing this entity's state is not initialized or has
        not yet returned a valid state, or if the hardware that implements commands
        from Home Assistant is not ready. Setting this property triggers
        :meth:`publish_availability()`."""
        return self._availability

    @availability.setter
    def availability(self, value: bool):
        self._availability = validators.validate_bool(value)

        self.logger.info(
            f"{self.COMPONENT} {self.object_id} {'available' if self._availability else 'unavailable'}"
        )

        try:
            self.publish_availability()
        except Exception as e:  # TODO: Narrow exceptions to catch
            self.logger.warning("Unable to publish availability.")

    @property
    def _state_topic(self) -> str:
        """Returns device-level state topic if a member of a device to allow batching
        of state updates, returns entity-level topic otherwise"""

        state_topic = ""
        try:
            self.logger.debug(f"State topic from device {self.device.device_id}")  # type: ignore
            state_topic = self.device.state_topic  # type: ignore
        except AttributeError:
            state_topic = f"entity/{self.object_id}/state"

        self.logger.debug(f"State topic: {state_topic}")
        return state_topic

    def announce(self):
        """Send MQTT discovery message for this entity only.

        Raises:
            ValueError : If the entity or its parent device does not have a valid
                ``mqtt_client`` set.
            RuntimeError : If the MQTT client is not connected
        """

        mqtt_client = self.mqtt_client

        if not isinstance(mqtt_client, MQTT):
            raise ValueError("mqtt_client not set")

        elif not mqtt_client.is_connected():
            raise RuntimeError("mqtt_client not connected")

        self.logger.debug(f"Using MQTT broker {mqtt_client.broker}")

        if self.device:
            discovery_topic = f"homeassistant/{self.COMPONENT}/{self.device.device_id}/{self.object_id}/config"
        else:
            discovery_topic = f"homeassistant/{self.COMPONENT}/{self.object_id}/config"

        self.logger.debug(f"Discovery topic: {discovery_topic}")

        discovery_payload = {
            "avty": [{"t": self.availability_topic}],
            "dev_cla": self.device_class,
            "en": self.enabled_by_default,
            "ent_cat": self.entity_category,
            "ic": self.icon,
            "name": self.name,
        }

        if self.device:
            self.logger.debug(f"Adding device config from {self.device.name}")
            discovery_payload.update(self.device.device_config)
            discovery_payload["avty"].append({"t": self.device.availability_topic})

        try:
            self._state  # type: ignore
            discovery_payload.update(
                {
                    "stat_t": self._state_topic,  # type: ignore
                    "val_tpl": f"{{{{ value_json.{self.object_id} }}}}",  # type: ignore
                }
            )
        except AttributeError:
            pass

        discovery_payload.update(self.component_config)

        self.logger.info(f"Publishing discovery message for {self.object_id}")
        self.logger.debug(f"Discovery paylods: {dumps(discovery_payload)}")
        self.mqtt_client.publish(discovery_topic, dumps(discovery_payload), True, 1)

    def publish_availability(self):
        """Explicitly publishes availability of the entity.

        This function is called automatically when :attr:`availability` property is
        changed.

        Returns:
            bool : :class:`True` if successful.
        """
        self.mqtt_client.publish(
            self.availability_topic,
            "online" if self.availability else "offline",
            True,
            1,
        )


class SensorEntity:
    """Parent class representing a Home Assistant Entity that publishes states"""

    def __init__(self, *args, **kwargs):

        self._state = None

        super().__init__(*args, **kwargs)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newstate):
        self._state = newstate
        try:
            self.publish_state()  # type: ignore
        except Exception as e:  # TODO: Narrow exception scope
            self.logger.warning("Unable to publish state change")  # type: ignore

    def publish_state(self):
        """Explicitly publishes state of the entity.

        This function is called automatically when :attr:`state` property is
        changed.

        Returns:
            bool : :class:`True` if successful.
        """
        self.mqtt_client.publish(  # type: ignore
            self._state_topic,  # type: ignore
            dumps({self.object_id: self._state}),  # type: ignore
            True,
            1,
        )


# class _CommandEntity(Entity):
#     """Parent class representing a Home Assistant Entity that accepts commands"""

#     pass
