import pytest
import minihass


def test_notImplemented():
    o = minihass.Device()
    with pytest.raises(NotImplementedError):
        o.announce()
