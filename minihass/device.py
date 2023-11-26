from adafruit_minimqtt.adafruit_minimqtt import MQTT


class Device:
    def __init__(
        self,
        device_id: str = "",
        name: str = "",
        mqtt_client: MQTT = "",
        connections: list[tuple[str, str]] = [],
    ):
        """A class representing a Home Assistant device

        :param device_id: Gloablly unique identifier for the Home Assistant device
        :type device_id: str, optional
        :param name: Device name
        :type name: str, optional
        :param mqtt_client: MMQTT object for communicating wiht
          Home Assistant
        :type mqtt_client: adafriut_minimqtt.adafruit_minimqtt.MQTT
        :param connections: List of tuples of Home Assistant device connections
            e.g. ``[('mac', 'de:ad:be:ef:d0:0d')]``
        :type connections: list[tuple(str, str)]
        """
        self.device_id = device_id
        self.name = name
        self.mqtt_client = mqtt_client
        self.connections = connections

    def announce(self, clean: bool = False):
        """Sends MQTT discovery messages for all device entities

        :param clean: Remove previously discovered entites that are no longer
            present, defaults to False
        :type clean: bool, optional
        :raises NotImplementedError: Not done yet
        """
        raise NotImplementedError
