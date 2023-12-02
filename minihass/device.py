from adafruit_minimqtt.adafruit_minimqtt import MQTT
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
        device_id (str, optional) : Gloablly unique identifier for the Home
            Assistant device. Auto-generated if not specified.
        name (str, optional) : Device name. Auto-generated if not specified.
        mqtt_client (adafruit_minimqtt.adafruit_minimqtt.MQTT, optional) : MMQTT
            object for communicating with Home Assistant. Defaults to ``""``.
        connections (list[tuple(str, str)], optiona;) : List of tuples of Home
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
        device_id: str = "",
        name: str = "",
        mqtt_client: MQTT = "",
        connections: list[tuple[str, str]] | None = None,
        entities: list[Entity] | None = None,
    ):

        self.device_id = device_id
        self.name = name
        self.mqtt_client = mqtt_client
        self.connections = connections if connections else []
        self._entities = entities if entities else []

    @property
    def entities(self) -> list[Entity]:
        """A list of :class:`Entity` objects associated with the device.

        This is a read-only property. Modify this property with the
        :meth:`add_entity()` and :meth:`delete_entity()` methods.

        Returns:
            list[Entity]: List of Entity subclasses.
        """
        return list(self._entities)

    def announce(self, clean: bool = False) -> bool:
        """Sends MQTT discovery messages for all device entities.

        Used immediately after connnecting to the MQTT broker to configure the
        corresponding entities in Home Assistant. Individual entities can be announced
        with their own :meth:`Entity.announce` methods.

        Args:
            clean (bool, optional) : Remove previously discovered entites that are no
                longer present. Defaults to :class:`False`.

        Raises:
            NotImplementedError : Not done yet.

        Returns:
            bool : :class:`True` if announcement succeeds, :class:`False` otherwise.
        """
        raise NotImplementedError

        return True
