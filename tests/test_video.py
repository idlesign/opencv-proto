import pytest

from ocvproto.exceptions import SourceError
from ocvproto.toolbox import Video, Image


def test_image(static_path, tmpdir):

    with pytest.raises(SourceError):
        with Video(static_path('empty')) as video:
            video.read()

    fpath_img = str(tmpdir / 'dumped.png')
    fpath_dump = str(tmpdir / 'dumped.avi')

    with Video(static_path('red.avi')) as video:

        assert video.height == 240
        assert video.width == 320
        assert video.fps == 25
        assert video.codec == 'FMP4'

        props = video.describe_properties()

        prop_fps = props['fps']
        assert prop_fps['default'] == 25
        assert prop_fps['max'] == 60
        prop_fps['callback'](60)

        video.dump_image(fpath_img)

        img = Image(fpath_img)
        assert img.height == 240

        video.dump_setup(fpath_dump)
        video.dump()
        video.dump(video)

    with Video(fpath_dump) as video:
        assert video.height == 240
        assert video.codec == 'XVID'
