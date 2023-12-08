"""Implements the binary_sensor MQTT component"""
from adafruit_minimqtt.adafruit_minimqtt import MQTT

from . import _validators as validators
from .entity import Entity, SensorEntity


class BinarySensor(Entity, SensorEntity):
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
        # name: str | None = None,
        # entity_category: str | None = None,
        # device_class: str | None = None,
        # object_id: str | None = None,
        # icon: str | None = None,
        # enabled_by_default: bool = True,
        # mqtt_client: MQTT | None = None,
        # logger_name: str = "minimqtt",
        # Component-specific arguments start here
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

        super().__init__(
            **kwargs
            # name=name,
            # entity_category=entity_category,
            # device_class=device_class,
            # object_id=object_id,
            # icon=icon,
            # enabled_by_default=enabled_by_default,
            # mqtt_client=mqtt_client,
        )
