import pytest

from ocvproto.exceptions import SourceError
from ocvproto.toolbox import Camera


@pytest.mark.xfail(reason='Camera open failure behavior depends on OpenCV backend')
def test_image(static_path):

    with pytest.raises(SourceError):
        with Camera() as cam:
            cam.read()
