# from micropython import const  # type: ignore
from adafruit_blinka import Enum as Enum

HA_MQTT_PREFIX = "homeassistant"


class QueueMode(Enum):
    NO: object = None
    YES: object = None
    ALWAYS: object = None


QueueMode.NO = QueueMode()
QueueMode.YES = QueueMode()
QueueMode.ALWAYS = QueueMode()
