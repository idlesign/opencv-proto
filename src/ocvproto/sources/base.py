from pathlib import Path
from typing import Union

from ..frame import Frame, OcvFrame, AnyFrame


class Source(Frame):
    """Basic source."""

    def __init__(self, src: Union[int, str, AnyFrame] = None):
        """

        :param src: Source id (int), path (str) or frame (np array)

        """
        frame = None

        if src is not None:
            if not isinstance(src, (str, int, Path)):
                frame, src = src, ''

            elif isinstance(src, Path):
                src = str(src)

        super().__init__(frame)

        if src is not 0:
            src = src or ''

        self._src = src

    @property
    def frame(self) -> OcvFrame:
        """Current frame."""
        frame = self._frame

        if frame is None:
            frame = self.read()._frame

        return frame

    def read(self) -> 'Source':  # pragma: nocover
        """Read and return current frame."""
        raise NotImplementedError
