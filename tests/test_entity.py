import os
from inspect import signature
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import adafruit_logging as logging
import pytest
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException

import minihass


class GenericEntity(minihass.entity.Entity):
    COMPONENT = "generic"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GenericSensor(minihass.entity.Entity, minihass.entity.SensorEntity):
    COMPONENT = "sensor"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@pytest.fixture
def entity(mqtt_client):
    e = GenericEntity(
        name="test", entity_category="config", object_id="foo", mqtt_client=mqtt_client
    )
    yield e


@pytest.fixture
def sensor(mqtt_client):
    s = GenericSensor(name="test", mqtt_client=mqtt_client)
    yield s


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

    expected_topic = "generic/foo1337d00d/availability"
    expected_msg = "online"
    entity.availability = True  # Set by property.setter
    assert entity.availability
    entity.mqtt_client.publish.assert_called_with(expected_topic, expected_msg, True, 1)


@patch("adafruit_logging.Logger.warning")
def test_Entity_availability_pub_failure(logger, entity):
    entity.mqtt_client.publish.side_effect = MMQTTException
    entity.availability = True
    logger.assert_called_with("Unable to publish availability.")


def test_Entity_auto_device_id():
    """Test object_id autogeneration from friendly name"""
    o = GenericEntity(name="Bar")
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
        GenericEntity()


def test_Entity_instantiate_parent():
    """Prevent direct instantiation of the Entity parent class"""
    with pytest.raises(RuntimeError):
        minihass.Entity()


def test_Entity_announce(mqtt_client):
    """Test publishing of MQTT dicsovery messages"""
    e = GenericEntity(name="Foo", mqtt_client=mqtt_client)
    expected_topic = "homeassistant/generic/foo1337d00d/config"
    expected_msg = '{"avty": [{"t": "generic/foo1337d00d/availability"}], "dev_cla": null, "en": true, "ent_cat": null, "ic": null, "name": "Foo"}'
    e.announce()
    mqtt_client.publish.assert_called_with(expected_topic, expected_msg, True, 1)


def test_Entity_announce_mqtt_client_disconnected(mqtt_client):
    """Throw exception if MQTT client is not connected"""
    e = GenericEntity(name="Foo", mqtt_client=mqtt_client)
    mqtt_client.is_connected.return_value = False
    with pytest.raises(RuntimeError):
        e.announce()


def test_Entity_announce_no_mqtt_client():
    """Throw an error if announce is called without an MQTT client object"""
    e = GenericEntity(name="Foo", mqtt_client=None)
    with pytest.raises(ValueError):
        e.announce()


def test_Entity_set_mqtt_client(mqtt_client):
    e = GenericEntity(name="foo")
    e.mqtt_client = mqtt_client
    assert e.mqtt_client == mqtt_client


def test_Entity_set_state(sensor):
    assert sensor.state == None
    sensor.state = "foobar"
    assert sensor.state == "foobar"


def test_SensorEntity_state_topic(sensor):
    assert sensor._state_topic == "entity/test1337d00d/state"


def test_SensorEntity_publish(sensor):
    sensor.state = "foo"
    sensor.mqtt_client.publish.assert_called_with(
        "entity/test1337d00d/state", '{"test1337d00d": "foo"}', True, 1
    )


def test_SensorEntity_queue(mqtt_client):
    s = GenericSensor(name="foo", queue="yes", mqtt_client=mqtt_client)
    mqtt_client.publish.side_effect = MMQTTException
    assert not s.state_queued
    s.state = "foo"
    assert s.state_queued
    mqtt_client.publish.side_effect = None
    s.publish_state()
    mqtt_client.publish.assert_called_with(
        "entity/foo1337d00d/state", '{"foo1337d00d": "foo"}', True, 1
    )
    assert not s.state_queued


def test_SensorEntity_always_queue(mqtt_client):
    s = GenericSensor(name="foo", queue="always", mqtt_client=mqtt_client)
    s.state = "foo"
    mqtt_client.publish.assert_not_called()
    s.publish_state()
    mqtt_client.publish.assert_called_with(
        "entity/foo1337d00d/state", '{"foo1337d00d": "foo"}', True, 1
    )
