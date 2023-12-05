import pytest
from adafruit_minimqtt.adafruit_minimqtt import MQTT

import minihass


@pytest.fixture
def entities():
    e = minihass.BinarySensor(name="foo")
    f = minihass.BinarySensor(name="bar")
    g = minihass.BinarySensor(name="baz")

    yield [e, f, g]


@pytest.fixture
def device():
    d = minihass.Device()
    yield d


def test_Device_instantiation(device):
    # Instantiate Device
    assert isinstance(device, minihass.Device)
    assert device.name == "MQTT Device"
    assert device.device_id == "mqtt_device1337d00d"


def test_Device_with_device_id():
    o = minihass.Device(device_id="foo")
    assert o.device_id == "foo"


def test_Device_entity_management(entities):

    o = minihass.Device(entities=entities)
    # # Ensure entities are populated
    for l in entities:
        assert l in o.entities


def test_Device_add_entity(entities):
    o = minihass.Device(entities=entities[:-1])
    assert o.add_entity(entities[-1]) == True
    assert entities[-1] in o.entities
    assert o.add_entity(entities[-1]) == False

    with pytest.raises(TypeError):
        o.add_entity(1)  # type: ignore


def test_Device_delete_entity(device, entities):
    device.add_entity(entities[0])

    assert device.delete_entity(entities[0]) == True
    assert device.delete_entity(entities[0]) == False


def test_Device_announce(entities):
    o = minihass.Device(entities=entities)
    assert entities[1] in o._entities
    assert o.announce()
