import pytest

from ocvproto.toolbox import Window, Trackbar


@pytest.mark.skip(reason='UI backend may be unavailable')
def test_trackbar(static_path):

    win = Window()
    win.create()

    log = []

    def call(val):
        log.append(val)

    tb = Trackbar('some', default=3, max=15, step=2, callback=call, keys='[]')
    tb.bind(win.name)
    assert int(tb) == 3
    assert float(tb) == 3
    assert bin(tb) == '0b11'

    tb.inc()
    assert tb.get_value() == 5

    tb.dec()
    assert tb.get_value() == 3

    assert log == [5, 3]
