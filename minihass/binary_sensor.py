"""Implements the binary_sensor MQTT component"""
from .entity import _Entity


class BinarySensor(_Entity):
    """Class representing a Home Assistant Binary Sensor

    :param name: Entity name
    :type name: str
    :param category: Entity category
    :type category: str, optional
    """

    def __init__(self, name: str = None, category: str = None):
        super().__init__(name=name, category=category)
        pass
