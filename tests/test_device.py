from unittest.mock import Mock, PropertyMock, patch

import pytest
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException

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
    mqtt_client.is_connected.return_value = False
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
    expected_topic = (
        "homeassistant/binary_sensor/mqtt_device1337d00d/bar1337d00d/config"
    )
    expected_payload = '{"avty": [{"t": "binary_sensor/bar1337d00d/availability"}, {"t": "device/mqtt_device1337d00d/availability"}], "en": true, "unique_id": "bar1337d00d", "name": "bar", "dev": {"ids": ["mqtt_device1337d00d"], "cns": []}, "stat_t": "device/mqtt_device1337d00d/state", "val_tpl": "{{ value_json.bar1337d00d }}", "expire_after": false, "force_update": false}'
    assert o.add_entity(entities[1]) == True
    mqtt_client.publish.assert_called_with(expected_topic, expected_payload, True, 1)
    assert entities[1] in o.entities


def test_Device_add_entity_already_exists(entities, mqtt_client):
    o = minihass.Device(entities=[entities[0]], mqtt_client=mqtt_client)
    assert o.add_entity(entities[0]) == False


@patch("adafruit_logging.Logger.error")
def test_Device_add_entity_mqtt_failure(logger, device, entities):
    device.mqtt_client.publish.side_effect = MMQTTException("something broke")
    assert device.add_entity(entities[2]) == True
    logger.assert_called_with("Announcement failed, ('something broke',)")


def test_Device_add_entity_wrong_type(device):
    with pytest.raises(TypeError):
        device.add_entity(1)  # type: ignore


def test_Device_delete_entity(device, entities):
    device.add_entity(entities[0])
    expected_topic = (
        f"homeassistant/binary_sensor/mqtt_device1337d00d/foo1337d00d/config"
    )
    device.mqtt_client.publish.side_effect = MMQTTException
    assert device.delete_entity(entities[0]) == True
    assert device.delete_entity(entities[0]) == False
    device.mqtt_client.publish.assert_called_with(expected_topic, "", True, 1)


def test_Device_announce(entities, mqtt_client):
    o = minihass.Device(
        entities=entities,
        mqtt_client=mqtt_client,
        hw_version="0.1",
        manufacturer="Genericor",
    )
    assert entities[1] in o._entities
    expected_topic = (
        "homeassistant/binary_sensor/mqtt_device1337d00d/baz1337d00d/config"
    )
    expected_msg = '{"avty": [{"t": "binary_sensor/baz1337d00d/availability"}, {"t": "device/mqtt_device1337d00d/availability"}], "en": true, "unique_id": "baz1337d00d", "name": "baz", "dev": {"ids": ["mqtt_device1337d00d"], "cns": [], "mf": "Genericor", "hw": "0.1"}, "stat_t": "device/mqtt_device1337d00d/state", "val_tpl": "{{ value_json.baz1337d00d }}", "expire_after": false, "force_update": false}'
    o.announce()
    mqtt_client.publish.assert_called_with(expected_topic, expected_msg, True, 1)


def test_Device_availability(device):
    assert not device.availability  # Set by constructor

    expected_topic = "device/mqtt_device1337d00d/availability"
    expected_msg = "online"
    device.availability = True  # Set by property.setter
    assert device.availability
    device.mqtt_client.publish.assert_called_with(expected_topic, expected_msg, True, 1)


@patch("adafruit_logging.Logger.error")
def test_Device_availability_pub_failure(logger, device):
    device.mqtt_client.publish.side_effect = MMQTTException("something failed")
    device.availability = True
    logger.assert_called_with("Availability publishing failed, ('something failed',)")


def test_Device_publish_state_queue(entities, mqtt_client):
    o = minihass.Device(entities=entities, mqtt_client=mqtt_client)
    mqtt_client.publish.side_effect = MMQTTException
    for e in entities:
        e.state = True
    mqtt_client.reset_mock()
    mqtt_client.publish.side_effect = None
    o.publish_state_queue()
    assert mqtt_client.publish.call_count == len(entities)
    mqtt_client.reset_mock()
    o.publish_state_queue()
    mqtt_client.publish.assert_not_called()


def test_Device_mqtt_on_connect_cb(entities, mqtt_client):
    o = minihass.Device(entities=[entities[-1]], mqtt_client=mqtt_client)
    mqtt_client.publish.side_effect = MMQTTException
    for e in entities:
        e.state = True
    mqtt_client.reset_mock()
    mqtt_client.publish.side_effect = None
    announce_topic = (
        "homeassistant/binary_sensor/mqtt_device1337d00d/baz1337d00d/config"
    )
    announce_msg = '{"avty": [{"t": "binary_sensor/baz1337d00d/availability"}, {"t": "device/mqtt_device1337d00d/availability"}], "en": true, "unique_id": "baz1337d00d", "name": "baz", "dev": {"ids": ["mqtt_device1337d00d"], "cns": []}, "stat_t": "device/mqtt_device1337d00d/state", "val_tpl": "{{ value_json.baz1337d00d }}", "expire_after": false, "force_update": false}'
    queue_topic = "device/mqtt_device1337d00d/state"
    queue_msg = '{"baz1337d00d": true}'
    availability_topic = "device/mqtt_device1337d00d/availability"
    availability_msg = "online"
    o.mqtt_on_connect_cb(mqtt_client, None, {}, 0)
    mqtt_client.publish.assert_any_call(announce_topic, announce_msg, True, 1)
    mqtt_client.publish.assert_any_call(queue_topic, queue_msg, True, 1)
    mqtt_client.publish.assert_any_call(availability_topic, availability_msg, True, 1)


@patch("adafruit_logging.Logger.error")
def test_Device_mqtt_on_connect_cb_error(logger, device):
    device.mqtt_on_connect_cb(device.mqtt_client, None, {}, 1)
    logger.assert_called_with(
        "MQTT client connection error: Connection Refused - Incorrect Protocol Version"
    )
