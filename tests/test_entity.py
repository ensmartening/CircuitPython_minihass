import os
from inspect import signature
from unittest.mock import Mock, PropertyMock, patch

import pytest
from adafruit_minimqtt.adafruit_minimqtt import MQTT

import minihass


@pytest.fixture
def entity(mqtt_client):
    e = minihass.BinarySensor(
        name="test", entity_category="config", object_id="foo", mqtt_client=mqtt_client
    )
    yield e


@pytest.fixture
def mqtt_client():
    mqtt_client = Mock(spec=MQTT)
    mqtt_client.is_connected.return_value = True
    p = PropertyMock(return_value="broker.example.com")
    mqtt_client.broker = p
    yield mqtt_client


def test_Entity_instantiation(entity):
    """Test basic Entity instantiation and sanity-check attributes"""
    assert isinstance(entity, minihass.Entity)
    assert entity.name == "test"
    assert entity.object_id == "foo1337d00d"


def test_Entity_availability(entity):
    assert not entity.availability  # Set by constructor

    expected_topic = "binary_sensor/foo1337d00d/availability"
    expected_msg = "online"
    entity.availability = True  # Set by property.setter
    assert entity.availability
    entity.mqtt_client.publish.assert_called_with(expected_topic, expected_msg, True, 1)


def test_Entity_auto_device_id():
    """Test object_id autogeneration from friendly name"""
    o = minihass.BinarySensor(name="Bar")
    assert o.object_id == "bar1337d00d"


@patch("microcontroller.cpu", spec="")
def test_Entity_auto_device_id_from_env(m):
    """Test chip ID environement variable from non-circuitpython instances"""
    with patch.dict(os.environ, {"CPU_UID": "deadbeef"}):
        assert minihass.Entity.chip_id() == "deadbeef"


@patch("microcontroller.cpu", spec="")
def test_Entity_auto_device_id_fail(m):
    """Test exception when chip ID can't be discovered"""
    with pytest.raises(RuntimeError):
        minihass.Entity.chip_id()


def test_Entity_no_name_or_device_id():
    """Throw error when neither name nor object_id are set"""
    with pytest.raises(ValueError):
        minihass.BinarySensor()


def test_Entity_signatures():
    """Verify that _Entity signature is a subset of all child classes"""
    e = signature(minihass.entity.Entity)
    for s in minihass.entity.Entity.__subclasses__():
        sp = signature(s)
        for p in e.parameters:
            assert p in sp.parameters


def test_Entity_instantiate_parent():
    """Prevent direct instantiation of the Entity parent class"""
    with pytest.raises(RuntimeError):
        minihass.Entity()


def test_Entity_announce(mqtt_client):
    """Test publishing of MQTT dicsovery messages"""
    e = minihass.BinarySensor(name="Foo", mqtt_client=mqtt_client)
    expected_topic = "homeassistant/binary_sensor/foo1337d00d/config"
    expected_msg = '{"avty": [{"t": "binary_sensor/foo1337d00d/availability"}], "dev_cla": null, "en": true, "ent_cat": null, "ic": null, "name": "Foo", "stat_t": "entity/foo1337d00d/state", "val_tpl": "{{ value_json.foo1337d00d }}", "expire_after": false, "force_update": false}'
    e.announce()
    mqtt_client.publish.assert_called_with(expected_topic, expected_msg, True, 1)


def test_Entity_announce_mqtt_client_disconnected(mqtt_client):
    """Throw exception if MQTT client is not connected"""
    e = minihass.BinarySensor(name="Foo", mqtt_client=mqtt_client)
    mqtt_client.is_connected.return_value = False
    with pytest.raises(RuntimeError):
        e.announce()


def test_Entity_announce_no_mqtt_client():
    """Throw an error if announce is called without an MQTT client object"""
    e = minihass.BinarySensor(name="Foo", mqtt_client=None)
    with pytest.raises(ValueError):
        e.announce()
