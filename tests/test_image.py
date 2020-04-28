import pytest

from ocvproto.exceptions import SourceError
from ocvproto.toolbox import Image


def test_image(static_path):
    img = Image(static_path('tiny.png'))
    assert img.height == 3
    assert img.width == 2

    with pytest.raises(SourceError):
        Image(static_path('empty')).read()
