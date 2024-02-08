"""Implements the binary_sensor MQTT component"""
from adafruit_minimqtt.adafruit_minimqtt import MQTT

from minihass.const import *

from . import _validators as validators
from .entity import Entity, StateEntity


class BinarySensor(StateEntity, Entity):
    """
    Class representing a Home Assistant Binary Sensor entity.

    .. note:: A :class:`BinarySensor` object takes all parameters from both the
        :class:`Entity` and :class:`StateEntity` classes, as well as the parameters
        listed below.

    Args:
        device_class (str, optional) : `Device class <https://www.home-assistant.io/integrations/binary_sensor/#device-class>`_
            of the entity. Defaults to :class:`None`
        force_update  (bool, optional) : Specifies whether the entity should be enabled
            when it is first added, defaults to :class:`False`.
        expire_after (int, optional) : Defines the number of seconds before the
            sensor's state expires, if it's not updated. After expiry, the sensor's
            state becomes unavailable. Defaults to ``0``.

    .. caution:: :class:`BinarySensor` and :class:`Sensor` entities will fail to set up
        if ``entity_category='config'``.
        `home‑assistant/core#107199 <https://github.com/home-assistant/core/pull/107199>`_

    """

    COMPONENT = "binary_sensor"

    def __init__(
        self,
        *args,
        device_class: str = "",
        force_update: bool = False,
        expire_after: int = 0,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        # self.expire_after = expire_after
        self.force_update = validators.validate_bool(force_update)

        # self.component_config = {
        #     "force_update": self.force_update,
        #     "pl_off": False,
        #     "pl_on": True,
        # }
        self.config.update(
            {
                CONFIG_FORCE_UPDATE: self.force_update,
                CONFIG_PAYLOAD_OFF: str(False),
                CONFIG_PAYLOAD_ON: str(True),
                CONFIG_EXPIRE_AFTER: expire_after,
            }
        )

        if device_class:
            self.config.update({CONFIG_DEVICE_CLASS: device_class})

        # if self.expire_after:
        #     self.component_config.update({"expire_after": "foo"})  # type: ignore

        # super().__init__(*args, **kwargs)

    @StateEntity.state.setter
    def state(self, state: bool):
        # state = validators.validate_bool(state)
        self._state_setter(str(bool(state)))  # type: ignore
