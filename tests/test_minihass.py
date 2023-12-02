import pytest
import minihass


def test_Entity():
    with pytest.raises(TypeError):
        o = minihass.Entity()

    o = minihass.BinarySensor(enabled_by_default=True)
    assert o.availability  # Set by constructor

    o.availability = False  # Set by property.setter
    assert not o.availability

    # Unimplemented functions
    with pytest.raises(NotImplementedError):
        o.announce()
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

    with pytest.raises(NotImplementedError):
        o.announce()
