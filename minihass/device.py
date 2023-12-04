from adafruit_minimqtt.adafruit_minimqtt import MQTT
from .entity import Entity
from . import _validators as validators
import microcontroller


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

    if hasattr(microcontroller, "cpu"):
        _chip_id = f"{int.from_bytes(microcontroller.cpu.uid, 'big'):x}"
    else:
        _chip_id = "1337d00d"  # for testing

    def __init__(
        self,
        mqtt_client: MQTT = "",
        device_id: str = "",
        name: str = "",
        manufacturer: str = None,
        hw_version: str = None,
        connections: list[tuple[str, str]] | None = None,
        entities: list[Entity] | None = None,
    ):

        self.name = validators.validate_string(name) if name else f"MQTT Device"

        if device_id:
            self.device_id = (
                f"{validators.validate_id_string(device_id)}{Device._chip_id}"
            )
        else:
            self.device_id = (
                f"{validators.validate_id_string(self.name)}{Device._chip_id}"
            )

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

    def add_entity(self, entity):
        """Add an entity to the device

        Args:
            Entity (Entity): Entity to add to the Home Assistant device
        """

        if isinstance(entity, Entity):
            self._entities.append(entity)
            entity.device_config = self.device_config
            entity.device_topic_path = f"{self.device_id}/"
            entity.state_topic = (f"device/{self.device_id}/state",)
            entity.announce()
        else:
            raise TypeError(f"Expected Entity, got {type(param).__name__}")

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
