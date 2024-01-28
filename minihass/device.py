from os import getenv

import adafruit_logging as logging
from adafruit_minimqtt.adafruit_minimqtt import CONNACK_ERRORS, MQTT, MMQTTException

from . import _validators as validators
from .const import *
from .entity import Entity, SensorEntity


class Device:
    """A class representing a Home Assistant device.

    A :class:`Device` represents a physical device with its own control unit, or a
    service. A CircuitPython-based microcontroller might provide multiple sensors, or
    expose multiple controls and services to Home Assistant; this would represent one
    device with multiple entities. In most cases you will only have one
    :class:`Device` object, although it it technically possible to create multiple
    objects in one instance of CircuitPython using this module.

    .. caution:: The MQTT client used to create a :class:`Device` object must not be
        connected at the time of instantiation. The devices uses a `Last Will and
        Testament`_ message to mark the device and its entities as ``unavailable`` after
        losing its connection to the MQTT broker, and the LWT is sent as part of the
        connection process.

    .. _Last Will and Testament: https://www.hivemq.com/blog/mqtt-essentials-part-9-last-will-and-testament/

    Args:
        mqtt_client (adafruit_minimqtt.adafruit_minimqtt.MQTT) : MMQTT
            object for communicating with Home Assistant.
        device_id (str, optional) : Gloablly unique identifier for the Home
            Assistant device. Auto-generated if not specified.
        name (str, optional) : Device name. Auto-generated if not specified.
        manufacturer (str, optional) : Device manufacturer to appear in Home
            Assistant's device registry. Defaults to :class:`None`
        hw_version (str, optional) : Device hardware version to appear in Home
            Assistant's device registry, Defaults to :class:`None`
        connections (list[tuple(str, str)], optional) : List of tuples of Home
            Assistant device connections e.g. ``[('mac', 'de:ad:be:ef:d0:0d')]``.
            Defaults to :class:`None`.
        entities (list[Entity], optional) : List of entity objects to include as
            part of the device. Defaults to :class:`None`

    Attributes:
        device_id (str) : Effective Device ID. Either normalized from the
            ``device_id`` parameter, or derived from ``name``
        mqtt_client (adafruit_minimqtt.adafruit_minimqtt.MQTT) : MQTT client.
        connections (list[tuple(str, str)]) : List of Home Aassistant device
            connections.
    """

    def __init__(
        self,
        mqtt_client: MQTT,
        device_id: str = "",
        name: str = "",
        manufacturer: str = "",
        hw_version: str = "",
        connections: list[tuple[str, str]] = [],
        entities: list[Entity] = [],
        logger_name: str = "minimqtt",
    ):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(getattr(logging, getenv("LOGLEVEL", ""), logging.WARNING))  # type: ignore
        self.name = validators.validate_string(name) if name else "MQTT Device"

        if device_id:
            self.device_id = f"{validators.validate_id_string(device_id)}"
        else:
            self.device_id = f"{validators.validate_id_string(self.name)}{Entity.chip_id()}"  # type: ignore

        self.manufacturer = validators.validate_string(manufacturer, null_ok=True)
        self.hw_version = validators.validate_string(hw_version, null_ok=True)
        self.mqtt_client = mqtt_client
        self.connections = connections if connections else []

        self.device_config = {
            "dev": {
                "ids": [self.device_id],
                "cns": self.connections,
            }
        }

        if self.manufacturer:
            self.device_config["dev"].update({"mf": self.manufacturer})

        if self.hw_version:
            self.device_config["dev"].update({"hw": self.hw_version})

        self._availability = False
        self.availability_topic = (
            f"{HA_MQTT_PREFIX}/device/{self.device_id}/availability"
        )
        self.state_topic = f"{HA_MQTT_PREFIX}/device/{self.device_id}/state"

        self.mqtt_client.will_set(self.state_topic, "offline", 1, True)
        self.mqtt_client.on_connect = self.mqtt_on_connect_cb  # type: ignore

        self._entities = []

        for entity in entities:
            self.add_entity(entity)

    @property
    def entities(self) -> list[Entity]:
        """A list of :class:`Entity` objects associated with the device.

        This is a read-only property. Modify this property with the
        :meth:`add_entity()` and :meth:`delete_entity()` methods.

        Returns:
            list[Entity]: List of Entity subclasses.
        """
        return list(self._entities)

    @property
    def availability(self) -> bool:
        """Availability of the device. Setting this entity to :class:`false` makes any
        entities belonging to this device appear as ``unavailable`` in Home Assistant.
        Setting this property triggers :meth:`publish_availability()`."""
        return self._availability

    @availability.setter
    def availability(self, value: bool):
        self._availability = validators.validate_bool(value)

        self.logger.warning(
            f"{self.device_id} {'available' if self._availability else 'unavailable'}"
        )

        try:
            self.publish_availability()
        except MMQTTException as e:
            self.logger.error(f"Availability publishing failed, {e.args}")

    def add_entity(self, entity: Entity) -> bool:
        """Add an entity to the device

        Args:
            Entity (Entity): Entity to add.

        Returns:
            bool: :class:`True` if the entity was added. :class:`False` if the entity
                is already a member of the device.
        """

        if isinstance(entity, Entity):
            if not entity in self._entities:
                self._entities.append(entity)
                entity.device = self
                entity.announce()
                return True
            else:
                return False
        else:
            raise TypeError(f"Expected Entity, got {type(entity).__name__}")

    def delete_entity(self, entity: Entity) -> bool:
        """Delete an entity from the device

        Args:
            entity (Entity): Entity to delete.

        Returns:
            bool: :class:`True` if the entity is deleted, :class:`False` if the entity
                was not a member of the device
        """
        if entity in self._entities:
            entity.withdraw()
            self._entities.remove(entity)
            entity.device = None
            return True
        else:
            return False

    def announce(self, clean: bool = False) -> bool:
        """Send MQTT discovery messages for all device entities.

        Used immediately after connnecting to the MQTT broker to configure the
        corresponding entities in Home Assistant. Individual entities can be announced
        with their own :meth:`Entity.announce()` methods.

        Args:
            clean (bool, optional) : Remove previously discovered entites that are no
                longer present. Defaults to :class:`False`.

        Returns:
            bool : :class:`True` if successful.
        """

        for entity in [x for x in self._entities]:
            entity.announce()

        return True

    def publish_state_queue(self) -> bool:
        """Publish any queued states for all device entities

        Returns:
            bool : :class:`True` if at least one sensor state was published.
        """

        ret = False
        for entity in (e for e in self.entities if isinstance(e, SensorEntity)): # TODO: based on existence of publisher
            if entity.state_queued:
                entity.publish_state()
                ret = True

        return ret

    def publish_availability(self):
        """Explicitly publishes availability of the device.

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

    def mqtt_on_connect_cb(self, mqtt_client, userdata, flags, rc):
        """Callback for the MQTT client's :attr:`on_connect` attribute. Sends
        announcement messages for all configured entities, publishes any outstanding
        entity states, and publishes its own availability as :class:`True`
        """

        if rc:
            self.logger.error(f"MQTT client connection error: {CONNACK_ERRORS[rc]}")
        else:
            self.announce()
            self.publish_state_queue()
            self.availability = True
