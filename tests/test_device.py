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


def test_Device_entity_management(entities):

    o = minihass.Device(entities=entities)
    # # Ensure entities are populated
    for l in entities:
        assert l in o.entities


def test_Device_add_entity(entities):
    o = minihass.Device(entities=entities[:-1])
    o.add_entity(entities[-1])

    assert entities[-1] in o.entities


def test_Device_announce(entities):
    o = minihass.Device(entities=entities)
    assert o.announce
