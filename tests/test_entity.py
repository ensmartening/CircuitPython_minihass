from inspect import signature

import pytest

import minihass


def test_Entity():
    with pytest.raises(RuntimeError):
        o = minihass.entity.Entity()

    o = minihass.BinarySensor(name="test")
    assert not o.availability  # Set by constructor

    o.availability = True  # Set by property.setter
    assert o.availability

    assert o.announce()

    with pytest.raises(NotImplementedError):
        o.publish_availability()


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
