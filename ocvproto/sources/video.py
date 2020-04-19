from pathlib import Path
from typing import Union

from .base import Source, TypeFrame
from .image import Image
from ..backend import cv
from ..exceptions import SourceError


class Video(Source):
    """Represents a video."""

    def __init__(self, src: Union[str, TypeFrame]):
        super().__init__(src)
        self._cap = None
        self._writer = None

    def __enter__(self) -> 'Video':
        self._cap = cv.VideoCapture(self._src)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cap.release()

        writer = self._writer

        if writer is not None:
            writer.release()

    def get_image(self) -> Image:
        """Returns image object from the current frame."""
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
        """FOURCC codec alias."""
        val = int(self._cap.get(cv.CAP_PROP_FOURCC))
        return ''.join([chr((val >> 8 * i) & 0xFF) for i in range(4)])

    def write_setup(
            self,
            fpath: Union[str, Path] = 'ocvproto.avi',
            *,
            width: int = None,
            height: int = None,
            fps: Union[int, float] = None,
            codec: str = 'XVID',
    ) -> cv.VideoWriter:
        """Configures write parameters.
        Returns opencv writer object.

        :param fpath: Filepath.
        :param width:
        :param height:
        :param fps: Frames per second.
        :param codec: FOURCC codec alias.

        """
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

    def write(self, frame: TypeFrame = None):
        """Writes the current or the given frame.
        Automatically configures writer object is needed.

        """
        if frame is None:
            frame = self.frame

        writer = self._writer
        if writer is None:
            writer = self.write_setup()

        writer.write(frame)

    def read(self) -> TypeFrame:
        success, frame = self._cap.read()

        if not success:
            raise SourceError(f"Unable to read from '{self._src}'.")

        self._frame = frame

        return frame
