import pytest
import minihass
from inspect import signature


def test_Entity():
    with pytest.raises(RuntimeError):
        o = minihass.entity._Entity()

    o = minihass.BinarySensor(name="test")
    assert not o.availability  # Set by constructor

    o.availability = True  # Set by property.setter
    assert o.availability

    assert o.announce(minihass.Device())

    with pytest.raises(NotImplementedError):
        o.publish_availability()


def test_BinarySensor():
    o = minihass.BinarySensor(name="test", entity_category="config")
    assert isinstance(o, minihass.BinarySensor)

def test_Entity_signatures():
    # Verify that _Entity signature is a subset of all child classes
    e = signature(minihass.entity._Entity)
    for s in minihass.entity._Entity.__subclasses__():
        sp = signature(s)
        for p in e.parameters:
            assert p in sp.parameters

def test_Device():
    e = minihass.BinarySensor(name="foo")
    f = minihass.BinarySensor(name="bar")
    g = minihass.BinarySensor(name="baz")

    # Instantiate Device
    o = minihass.Device(entities=[e, f])
    assert isinstance(o, minihass.Device)

    # Ensure entities are populated
    l = o.entities
    assert e in l
    assert f in l

    # Ensure Device.entities is immmutable
    l.append(g)
    l = o.entities
    assert g not in l

    assert o.announce()
