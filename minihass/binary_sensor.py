"""Implements the binary_sensor MQTT component"""
from .entity import _Entity
from . import _validators as validators


class BinarySensor(_Entity):
    """Class representing a Home Assistant Binary Sensor

    :param name: Entity Name. Can be null if only device name is relevant
    :type name: str, optional
    :param entity_category: Set to speficy ``DIAGNOSTIC`` or ``CONFIG`` entites
    :type entity_category: str, optional
    :param object_id: Set to generate ``entity_id`` from ``object_id`` instead of ``name``
    :type object_id: str, optional
    :param unique_id_suffix: The entity's ``unique_id`` is genrated by concatenating
        ``name`` or ``object_id`` onto the device's unique identifier. Set to use a
        different string, or if ``name`` and ``object_id`` are both :class:`None`
    :type unique_id_suffix: str, optional
    :param icon: Override the device domain default icon
    :type icon: str, optional
    :param force_update: Send update events even when the state hasn't changed,
        defaults to :class:`False`
    :type force_update: bool, optional
    :param enabled_by_default: Specifies whether the entity should be enabled when it
        is first added, defaults to :class:`False`
    :type enabled_by_default: bool, optional
    :param expire_after: Defines the number of seconds after the sensor's state
        expires, if it's not updated. After expiry, the sensor's state becomes
        unavailable. Defaults to :class:`False`.
    :type expire_after: bool, optional
    """

    def __init__(
        self,
        name: str = None,
        category: str = None,
        object_id: str = None,
        unique_id_prefix: str = None,
        icon: str = None,
        force_update: bool = False,
        enabled_by_default: bool = False,
        expire_after: int = None,
    ):

        super().__init__(
            name=name,
            category=category,
            object_id=object_id,
            unique_id_prefix=unique_id_prefix,
            icon=icon,
            force_update=force_update,
            enabled_by_default=enabled_by_default,
        )

        self.expire_after = validators.validate_bool(expire_after)
