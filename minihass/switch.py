"""Implements the switch MQTT Component"""

from adafruit_minimqtt.adafruit_minimqtt import MQTT

from minihass.const import *

from . import _validators as validators
from .entity import Entity, StateEntity, CommandEntity

class Switch(CommandEntity, StateEntity, Entity):
    """
    Class representing a Home Assistant Switch entity

    .. note:: A :class:`Switch` object takes all parameters from the
        :class:`Entity`, :class:`StateEntity`, and :class:`CommandEntity`
        classes, as well as the parameters listed below.

    Args:
        CommandEntity (_type_): _description_
        StateEntity (_type_): _description_
        Entity (_type_): _description_foo
    """    
    pass

    COMPONENT = "switch"

    def __init__(
        self,
        *args,
        device_class: str = "",
        force_update: bool = False,
        expire_after: int = 0,
        **kwargs
    ):
        """_summary_

        Args:
            device_class (str, optional): _description_. Defaults to "".
            force_update (bool, optional): _description_. Defaults to False.
            expire_after (int, optional): _description_. Defaults to 0.
        """        
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

