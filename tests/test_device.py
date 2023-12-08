from unittest.mock import Mock, PropertyMock, patch

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
def device(mqtt_client):
    d = minihass.Device(mqtt_client=mqtt_client)
    yield d


@pytest.fixture
def mqtt_client():
    mqtt_client = Mock(spec=MQTT)
    mqtt_client.is_connected.return_value = True
    p = PropertyMock(return_value="broker.example.com")
    mqtt_client.broker = p

    yield mqtt_client


def test_Device_instantiation(device):
    # Instantiate Device
    assert isinstance(device, minihass.Device)
    assert device.name == "MQTT Device"
    assert device.device_id == "mqtt_device1337d00d"


def test_Device_with_device_id(mqtt_client):
    o = minihass.Device(device_id="foo", mqtt_client=mqtt_client)
    assert o.device_id == "foo"


def test_Device_entity_management(entities, mqtt_client):

    o = minihass.Device(entities=entities, mqtt_client=mqtt_client)
    # # Ensure entities are populated
    for l in entities:
        assert l in o.entities


def test_Device_add_entity(entities, mqtt_client):
    o = minihass.Device(entities=[entities[0]], mqtt_client=mqtt_client)
    assert o.add_entity(entities[1]) == True
    assert entities[1] in o.entities
    assert o.add_entity(entities[1]) == False

    with pytest.raises(TypeError):
        o.add_entity(1)  # type: ignore

    mqtt_client.publish.side_effect = RuntimeError
    assert o.add_entity(entities[2]) == True


def test_Device_delete_entity(device, entities):
    device.add_entity(entities[0])

    assert device.delete_entity(entities[0]) == True
    assert device.delete_entity(entities[0]) == False


def test_Device_announce(entities, mqtt_client):
    o = minihass.Device(entities=entities, mqtt_client=mqtt_client)
    assert entities[1] in o._entities
    expected_topic = (
        "homeassistant/binary_sensor/mqtt_device1337d00d/baz1337d00d/config"
    )
    expected_msg = '{"avty": [{"t": "binary_sensor/baz1337d00d/availability"}, {"t": "device/mqtt_device1337d00d/availability"}], "dev_cla": null, "en": true, "ent_cat": null, "ic": null, "name": "baz", "dev": {"mf": null, "hw": null, "ids": ["mqtt_device1337d00d"], "cns": []}, "stat_t": "device/mqtt_device1337d00d/state", "val_tpl": "{{ value_json.baz1337d00d }}", "expire_after": false, "force_update": false}'
    o.announce()
    mqtt_client.publish.assert_called_with(expected_topic, expected_msg, True, 1)
