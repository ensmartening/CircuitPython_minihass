import pytest
import minihass


def test_notImplemented():
    o = minihass.Device()
    with pytest.raises(NotImplementedError):
        o.announce()


def test_BinarySensor():
    o = minihass.BinarySensor(name="test", category="config")
    assert isinstance(o, object)
