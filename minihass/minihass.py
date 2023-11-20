'''
This module provides classes to define devices and entities to be exposed
to Home Assistant over MQTT in CircuitPython, as well as methods to publish
states and availability for those entities.
'''
from adafruit_minimqtt.adafruit_minimqtt import MQTT

class Device(object):
    '''A class representing a Home Assistant device
    
    :param device_id: Gloablly unique identifier for the Home Assistant device
    :type device_id: str
    :param name: Device name
    :type name: str
    :param mqtt_client: MMQTT object for communicating wiht Home Assistant
    :type mqtt_client: adafruit_minimqtt.adafruit_minimqtt.MQTT
    :param connections: List of tuples of Home Assistant device connections
        e.g. ``[('mac', 'de:ad:be:ef:d0:0d')]``
    :type connections: list[tuple(str, str)]

    Properties
    ----------

    device_id : str
        Gloablly unique identifier for the Home Assistant device
    name : str
        Friendly name of the device
    mqtt_client : adafruit_minimqtt.adafruit_minimqtt.MQTT
        MMQTT object for communicating with Home Assistant
    connections : list of (str, str)
        List of Home Assistant Device Connections
        e.g.: `[('mac', 'de:ad:be:ef:d0:0d')]`
    entities : list of d
        

    Methods
    -------

    announce(clean: bool = False)
        Sends MQTT discovery messages for all device entities

    '''

    def __init__(
            self,
            device_id: str = None,
            name: str = None,
            mqtt_client: MQTT = None,
            connections: list[tuple[str, str]] = []
    ):
        self.device_id = device_id
        self.name = name
        self.mqtt_client = mqtt_client
        self.connections = connections

    def announce(self, clean: bool = False):
        raise NotImplementedError

class _Entity:
    '''
    Parent class for other component entities (sensor, binary_sensor, etc)

    Attributes
    ----------
    
    Methods
    -------
    '''

    def __init__(
            self
    ):
        pass

class BinarySensor(_Entity):
    '''
    Class representing a binary sensor.

    Attributes
    ----------

    Methods
    -------

    Also inherits attributes and methods from the base entity class:

    '''
    __doc__ += _Entity.__doc__

    pass