import os
from email.iterators import body_line_iterator
from inspect import signature
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import adafruit_logging as logging
import pytest
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException

import minihass


@pytest.fixture
def binary_sensor(mqtt_client):
    e = minihass.BinarySensor(
        name="test",
        entity_category="config",
        object_id="foo",
        mqtt_client=mqtt_client,
        device_class="temperature",
        expire_after=1,
    )
    yield e


@pytest.fixture
def mqtt_client():
    mqtt_client = Mock(spec=MQTT)
    mqtt_client.is_connected.return_value = True
    p = PropertyMock(return_value="broker.example.com")
    mqtt_client.broker = p
    yield mqtt_client


def test_Entity_instantiation(binary_sensor):
    """Test basic Entity instantiation and sanity-check attributes"""
    assert isinstance(binary_sensor, minihass.BinarySensor)
    assert binary_sensor.name == "test"
    assert binary_sensor.object_id == "foo1337d00d"


def test_Entity_state(binary_sensor):
    """Test publishing of MQTT state message"""
    expected_topic = "homeassistant/foo1337d00d/state"
    expected_msg = "True"
    binary_sensor.state = "yes"
    binary_sensor.mqtt_client.publish.assert_called_with(
        expected_topic, expected_msg, True, 1
    )


def test_Entity_announce(binary_sensor):
    """Test publishing of MQTT discovery messages"""
    expected_topic = "homeassistant/binary_sensor/foo1337d00d/config"
    expected_msg = '{"avty": [{"t": "homeassistant/foo1337d00d/availability"}], "en": true, "unique_id": "foo1337d00d", "e": "utf-8", "name": "test", "ent_cat": "config", "stat_t": "homeassistant/foo1337d00d/state", "force_update": false, "pl_off": "False", "pl_on": "True", "expire_after": 1, "dev_cla": "temperature"}'
    binary_sensor.announce()
    binary_sensor.mqtt_client.publish.assert_called_with(
        expected_topic, expected_msg, True, 1
    )
