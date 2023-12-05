from inspect import signature

import pytest

import minihass


@pytest.fixture
def entity():
    e = minihass.BinarySensor(name="test", entity_category="config", object_id="foo")
    yield e


def test_Entity_instantiation(entity):

    assert isinstance(entity, minihass.Entity)
    assert entity.name == "test"
    assert entity.object_id == "foo1337d00d"

    assert not entity.availability  # Set by constructor

    entity.availability = True  # Set by property.setter
    assert entity.availability

    assert entity.announce()

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
