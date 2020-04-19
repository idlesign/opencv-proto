from pathlib import Path
from typing import Union

import cv2 as cv

from ._base import Source
from .image import Image
from ..exceptions import SourceError


class Video(Source):
    """Video source."""

    def __init__(self, src):
        super().__init__(src)
        self._cap = None
        self._writer = None

    def __enter__(self):
        self._cap = cv.VideoCapture(self._src)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cap.release()

        writer = self._writer

        if writer is not None:
            writer.release()

    def get_image(self) -> Image:
        return Image(self.frame)

    @property
    def hue(self) -> int:
        return int(self._cap.get(cv.CAP_PROP_HUE))

    @property
    def saturation(self) -> int:
        return int(self._cap.get(cv.CAP_PROP_SATURATION))

    @property
    def contrast(self) -> int:
        return int(self._cap.get(cv.CAP_PROP_CONTRAST))

    @property
    def brightness(self) -> int:
        return int(self._cap.get(cv.CAP_PROP_BRIGHTNESS))

    @property
    def pos(self) -> int:
        return int(self._cap.get(cv.CAP_PROP_POS_MSEC))

    @property
    def width(self) -> int:
        return int(self._cap.get(cv.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self) -> int:
        return int(self._cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    @property
    def fps(self) -> Union[int, float]:
        return self._cap.get(cv.CAP_PROP_FPS)

    @property
    def codec(self) -> str:
        val = int(self._cap.get(cv.CAP_PROP_FOURCC))
        return ''.join([chr((val >> 8 * i) & 0xFF) for i in range(4)])

    def write_setup(
            self,
            fpath: Union[str, Path] = 'out.avi',
            *,
            width: int = None,
            height: int = None,
            fps: Union[int, float] = None,
            codec: str = 'XVID',
    ):

        if codec is None:
            codec = self.codec

        fcc = cv.VideoWriter_fourcc(*codec)

        writer = cv.VideoWriter(
            f'{fpath}',
            fcc,
            fps or self.fps,
            (width or self.width, height or self.height)
        )
        self._writer = writer
        return writer

    def write(self, frame=None):
        if frame is None:
            frame = self.frame

        writer = self._writer
        if writer is None:
            writer = self.write_setup()

        writer.write(frame)

    def read(self):
        success, frame = self._cap.read()

        if not success:
            raise SourceError(f"Unable to read from '{self._src}'.")

        self._frame = frame

        return frame
