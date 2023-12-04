import pytest
import minihass


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
    o = minihass.BinarySensor(name="test", category="config")
    assert isinstance(o, minihass.BinarySensor)


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
