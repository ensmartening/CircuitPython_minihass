from adafruit_minimqtt.adafruit_minimqtt import MQTT

from . import _validators as validators
from .entity import Entity


class Device:
    """A class representing a Home Assistant device.

    A :class:`Device` represents a physical device with its own control unit, or a
    service. A CircuitPython-based microcontroller might provide multiple sensors, or
    expose multiple controls and services to Home Assistant; this would represent one
    device with multiple entities. In most cases you will only have one
    :class:`Device` object, although it it technically possible to create multiple
    objects in one instance of CircuitPython using this module.

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
        device_id (str) : Effective Device ID.
        name (str) : Effective device name.
        mqtt_client (adafruit_minimqtt.adafruit_minimqtt.MQTT) : MQTT client.
        connections (list[tuple(str, str)]) : List of Home Aassistant device
            connections.
    """

    def __init__(
        self,
        mqtt_client: MQTT,
        device_id: str = "",
        name: str = "",
        manufacturer: str | None = None,
        hw_version: str | None = None,
        connections: list[tuple[str, str]] | None = None,
        entities: list[Entity] = [],
    ):

        self.name = validators.validate_string(name) if name else "MQTT Device"

        if device_id:
            self.device_id = f"{validators.validate_id_string(device_id)}"
        else:
            self.device_id = f"{validators.validate_id_string(self.name)}{Entity.chip_id()}"  # type: ignore

        self.manufacturer = validators.validate_string(manufacturer, none_ok=True)
        self.hw_version = validators.validate_string(hw_version, none_ok=True)
        self.mqtt_client = mqtt_client
        self.connections = connections if connections else []

        self.device_config = {
            "dev": {
                "mf": self.manufacturer,
                "hw": self.hw_version,
                "ids": [self.device_id],
                "cns": self.connections,
            }
        }
        self.availability_topic = f"device/{self.device_id}/availability"
        self.state_topic = f"device/{self.device_id}/state"
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
