"""
Defines base classes for components that only publish shates (e.g. sensors),
as well as components that accept commands (e.g. switches)
"""
from __future__ import annotations

from json import dumps
from os import getenv

import adafruit_logging as logging
import microcontroller
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException

from . import _validators as validators
from .const import *

# from queue import Queue




class Entity(object):
    """Parent class for child classes representing Home Assistant entities. Cannot be
    instantiated directly.

    Args:
        name (int, optional) : Entity Name. Can be null if only the device name is
            relevant. One of ``name`` or ``object_id`` must be set.
        encoding (str, optional) : Set to specify encoding of payloads. Defaults to
            ``utf-8``
        entity_category (str, optional) : Set to specify ``DIAGNOSTIC`` or ``CONFIG``
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
        name: str = "",
        entity_category: str = "",
        encoding: str = "utf-8",
        object_id: str = "",
        icon: str = "",
        enabled_by_default: bool = True,
        mqtt_client: MQTT | None = None,
        logger_name: str = "minimqtt",
        **kwargs,
    ):
        try:
            self.logger
        except AttributeError:
            self.logger = logging.getLogger(logger_name)
            self.logger.setLevel(getattr(logging, getenv("LOGLEVEL", ""), logging.WARNING))  # type: ignore

        if self.__class__ == Entity:
            self.logger.error(
                "Attepted instantiation of parent class, raising an exception..."
            )
            raise RuntimeError("Entity class cannot be raised on its own")

        self.name = validators.validate_string(name, null_ok=True)
        self.logger.debug(f"Entity name: self.name")

        # self.entity_category = validators.validate_entity_category(entity_category)
        # self.logger.debug(f"Entity category: {self.entity_category}")

        # self.device_class = validators.validate_string(device_class, null_ok=True)
        # self.logger.debug(f"Entity device_class: {self.device_class}")

        # self.encoding = encoding
        # self.logger.debug(f"Entity encoding: {self.encoding}")

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

        self.icon = validators.validate_string(icon, null_ok=True)
        self.logger.debug(f"Entity icon: {self.icon}")

        self.enabled_by_default = validators.validate_bool(enabled_by_default)
        self.logger.debug(
            f"Entity {'enabled' if self.enabled_by_default else 'disabled'} by default"
        )

        # self.availability_topic = (
        #     f"{HA_MQTT_PREFIX}/{self.object_id}/availability"
        # )

        self.config = {
            CONFIG_AVAILABILITY: [
                {"t": f"{HA_MQTT_PREFIX}/{self.object_id}/availability"}
            ],
            CONFIG_ENABLED_BY_DEFAULT: self.enabled_by_default,
            CONFIG_UNIQUE_ID: self.object_id,
            CONFIG_ENCODING: encoding,
        }

        if self.name:
            self.config.update({CONFIG_NAME: self.name})

        if entity_category:
            self.config.update({CONFIG_ENTITY_CATEGORY: entity_category})

        if self.icon:
            self.config.update({CONFIG_ICON: self.icon})

        self._mqtt_client = mqtt_client
        try:
            self.logger.debug(f"Entity MQTT client: {self._mqtt_client.broker}")  # type: ignore
        except AttributeError:
            self.logger.debug(
                f"MQTT{' broker' if self._mqtt_client else '_client'} not set"
            )

        self._availability = False

        self.device: "Device" | None = None  # type: ignore

        try:
            self.component_config
        except AttributeError:
            self.component_config = {}

        self.logger.info(f"Initialized {self.name}: {self.object_id} ")
        self.logger.warning(f"args: {args}, kwargs: {kwargs}")

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
        entity appear as ``unavailable`` in Home Assistant. This may be desired if, for
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
        except AttributeError:
            self.logger.warning("Unable to publish availability - MQTT client not set")
        except MMQTTException as e:
            self.logger.error(f"Availability publishing failed, {e.args}")

    # @property
    # def _state_topic(self) -> str:
    #     """Returns device-level state topic if a member of a device to allow batching
    #     of state updates, returns entity-level topic otherwise"""

    #     state_topic = ""
    #     try:
    #         self.logger.debug(f"State topic from device {self.device.device_id}")  # type: ignore
    #         state_topic = self.device.state_topic  # type: ignore
    #     except AttributeError:
    #         state_topic = f"{HA_MQTT_PREFIX}/entity/{self.object_id}/state"

    #     self.logger.debug(f"State topic: {state_topic}")
    #     return state_topic

    def announce(self):
        """Send MQTT discovery message for this entity only.

        Raises:
            ValueError : If the entity or its parent device does not have a valid
                ``mqtt_client`` set.
            RuntimeError : If the MQTT client is not connected
        """

        try:
            self.logger.debug(f"Using MQTT broker {self.mqtt_client.broker}")
        except AttributeError:
            self.logger.warning("MQTT client not set")

        if self.device:
            discovery_topic = f"{HA_MQTT_PREFIX}/{self.COMPONENT}/{self.device.device_id}/{self.object_id}/config"
        else:
            discovery_topic = (
                f"{HA_MQTT_PREFIX}/{self.COMPONENT}/{self.object_id}/config"
            )

        self.logger.debug(f"Discovery topic: {discovery_topic}")

        # discovery_payload = {
        #     "avty": [{"t": self.availability_topic}],
        #     "en": self.enabled_by_default,
        #     "unique_id": self.object_id,
        #     "e": self.encoding,
        # }

        # if self.name:
        #     discovery_payload.update({"name": self.name})

        # if self.device_class:
        #     discovery_payload.update({"dev_cla": self.device_class})

        # if self.entity_category:
        #     discovery_payload.update({"ent_cat": self.entity_category})

        # if self.icon:
        #     discovery_payload.update({"ic": self.icon})

        # if self.device:
        #     self.logger.debug(f"Adding device config from {self.device.name}")
        #     discovery_payload.update(self.device.device_config)
        #     discovery_payload["avty"].append({"t": self.device.availability_topic})

        # try:
        #     self._state  # type: ignore
        #     discovery_payload.update(
        #         {
        #             "stat_t": self._state_topic,  # type: ignore
        #             # "val_tpl": f"{{{{ value_json.{self.object_id} }}}}",  # type: ignore
        #         }
        #     )
        # except AttributeError:
        #     pass
        # discovery_payload.update(self.component_config)
        self.logger.warning(f"self.config: {dumps(self.config)}")
        # self.logger.warning(f'discovery_payload: {dumps(discovery_payload)}')
        self.logger.info(f"Publishing discovery message for {self.object_id}")
        # self.logger.debug(f"Discovery payload: {dumps(discovery_payload)}")
        try:
            self.mqtt_client.publish(discovery_topic, dumps(self.config), True, 1)
        except AttributeError:
            self.logger.warning("Unable to announce: - MQTT client not set")
        except MMQTTException as e:
            self.logger.error(f"Announcement failed, {e.args}")

    def withdraw(self):
        """Send MQTT discovery message to remove this entity.

        Raises:
            ValueError : If the entity or its parent device does not have a valid
                ``mqtt_client`` set.
            RuntimeError : If the MQTT client is not connected
        """

        try:
            self.logger.debug(f"Using MQTT broker {self.mqtt_client.broker}")
        except AttributeError:
            self.logger.warning("MQTT client not set")

        if self.device:
            discovery_topic = f"{HA_MQTT_PREFIX}/{self.COMPONENT}/{self.device.device_id}/{self.object_id}/config"
        else:
            discovery_topic = (
                f"{HA_MQTT_PREFIX}/{self.COMPONENT}/{self.object_id}/config"
            )

        self.logger.info(f"Publishing withdrawal message for {self.object_id}")
        try:
            self.mqtt_client.publish(discovery_topic, "", True, 1)
        except AttributeError:
            self.logger.warning("Unable to withdraw: - MQTT client not set")
        except MMQTTException as e:
            self.logger.error(f"Withdrawal failed, {e.args}")

    def publish_availability(self):
        """Explicitly publishes availability of the entity.

        This function is called automatically when :attr:`availability` property is
        changed.

        Returns:
            bool : :class:`True` if successful.
        """
        self.mqtt_client.publish(
            self.config[CONFIG_AVAILABILITY][0][CONFIG_TOPIC],
            "online" if self.availability else "offline",
            True,
            1,
        )


class StateEntity(Entity):
    """Mixin class implementing state publishing

    Args:
        queue ("yes"|"no"|"always", optional): Controls state queuing behaviour.
            If ``"yes"``, if publishing to the MQTT broker fails, the message will
            be queued and can be re-published, by calling the device's
            :meth:`Device.publish_state_queue()` method. If ``"no"``, unpublished states
            are not queued, but can still be explicitly published by calling the
            entity's :meth:`publish_state` method. If ``"always"``, states are not
            automatically published and will alawys be queued. Defaults to
            ``"yes"``.
    """

    def __init__(
        self, *args, queue_mode=QueueMode.YES, logger_name="minimqtt", **kwargs
    ):
        try:
            self.logger
        except AttributeError:
            self.logger = logging.getLogger(logger_name)
            self.logger.setLevel(getattr(logging, getenv("LOGLEVEL", ""), logging.WARNING))  # type: ignore

        if self.__class__ == StateEntity:
            self.logger.error(  # type: ignore
                "Attepted instantiation of parent class, raising an exception..."
            )
            raise RuntimeError("StateEntity class cannot be raised on its own")

        super().__init__(*args, **kwargs)

        self.queue_mode = queue_mode
        self._state: object = None
        self.state_queued: bool = False

        self.config.update(
            {CONFIG_STATE_TOPIC: f"{HA_MQTT_PREFIX}/{self.object_id}/state"}
        )

        # super().__init__(*args, **kwargs)

    def _state_getter(self):
        """Gets or sets the state of a sensor entity. Setting this parameter calls
        :meth:`publish_state()`"""
        return self._state

    def _state_setter(self, newstate):
        self._state = newstate

        if self.queue_mode == QueueMode.ALWAYS:
            self.state_queued = True
        else:
            try:
                self.publish_state()  # type: ignore
            except Exception as e:  # TODO: Narrow exception scope
                if self.queue_mode != QueueMode.NO:
                    self.state_queued = True
                self.logger.warning("Unable to publish state change")  # type: ignore

    state = property(_state_getter, _state_setter)

    def publish_state(self):
        """Explicitly publishes state of the entity.

        This function is called automatically when :attr:`state` property is
        changed.
        """
        self.mqtt_client.publish(  # type: ignore
            self.config[CONFIG_STATE_TOPIC],  # type: ignore
            self._state,  # type: ignore
            True,
            1,
        )
        self.state_queued = False
