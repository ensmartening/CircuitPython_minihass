"""Implements the binary_sensor MQTT component"""
from adafruit_minimqtt.adafruit_minimqtt import MQTT

from . import _validators as validators
from .entity import SensorEntity


class BinarySensor(SensorEntity):
    """
    Class representing a Home Assistant Binary Sensor entity.

    .. note:: A :class:`BinarySensor` object takes all parameters from both the
        :class:`Entity` and :class:`SensorEntity` classes, as well as the parameters
        listed below.

    Args:
        force_update  (bool, optional) : Specifies whether the entity should be enabled
            when it is first added, defaults to :class:`False`.
        expire_after (bool, optional) : Defines the number of seconds after the
            sensor's state expires, if it's not updated. After expiry, the sensor's
            state becomes unavailable. Defaults to :class:`False`.

    """

    COMPONENT = "binary_sensor"

    def __init__(
        self,
        *args,
        force_update: bool = False,
        expire_after: int | None = None,
        **kwargs
    ):
        self.expire_after = validators.validate_bool(expire_after)
        self.force_update = validators.validate_bool(force_update)

        self.component_config = {
            "expire_after": self.expire_after,
            "force_update": self.force_update,
        }

        super().__init__(*args, **kwargs)

    @SensorEntity.state.setter
    def state(self, state):
        state = validators.validate_bool(state)
        self._state_setter(state)  # type: ignore
