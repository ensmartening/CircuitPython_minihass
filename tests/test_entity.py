from inspect import signature
from unittest.mock import MagicMock, Mock

import pytest
from adafruit_minimqtt.adafruit_minimqtt import MQTT

import minihass


@pytest.fixture
def entity():
    e = minihass.BinarySensor(name="test", entity_category="config", object_id="foo")
    yield e


@pytest.fixture
def mqtt_client():
    mqtt_client = Mock(spec=MQTT)
    mqtt_client.is_connected.return_value = True

    yield mqtt_client


def test_Entity_instantiation(entity):

    assert isinstance(entity, minihass.Entity)
    assert entity.name == "test"
    assert entity.object_id == "foo1337d00d"

    assert not entity.availability  # Set by constructor

    entity.availability = True  # Set by property.setter
    assert entity.availability

    with pytest.raises(NotImplementedError):
        entity.publish_availability()


def test_Entity_auto_device_id():
    o = minihass.BinarySensor(name="bar")
    assert o.object_id == "bar1337d00d"


def test_Entity_auto_device_id_fail():
    with pytest.raises(ValueError):
        o = minihass.BinarySensor()


def test_BinarySensor():
    o = minihass.BinarySensor(name="test", entity_category="config")
    assert isinstance(o, minihass.BinarySensor)


def test_Entity_signatures():
    # Verify that _Entity signature is a subset of all child classes
    e = signature(minihass.entity.Entity)
    for s in minihass.entity.Entity.__subclasses__():
        sp = signature(s)
        for p in e.parameters:
            assert p in sp.parameters


def test_Entity_instantiate_parent():
    with pytest.raises(RuntimeError):
        minihass.Entity()


def test_publish(mqtt_client):
    e = minihass.BinarySensor(name="Foo", mqtt_client=mqtt_client)
    expected_topic = "homeassistant/binary_sensor/foo1337d00d/config"
    expected_msg = '{"avty": [{"t": "binary_sensor/foo1337d00d/availability"}], "dev_cla": null, "en": true, "ent_cat": null, "ic": null, "name": "Foo", "stat_t": "entity/foo1337d00d/state", "val_tpl": "{{ value_json.foo1337d00d }}", "expire_after": false, "force_update": false}'
    e.announce()
    mqtt_client.publish.assert_called_with(expected_topic, expected_msg, True, 1)
