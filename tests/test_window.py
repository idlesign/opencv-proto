import pytest

from ocvproto.toolbox import Window


@pytest.mark.skip(reason='UI backend may be unavailable')
def test_window():
    win = Window()
    win.create(autosize=False)
    win.position(x=10, y=20)
    win.resize(width=50, height=50)

