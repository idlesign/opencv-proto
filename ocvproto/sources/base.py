from typing import Union

from ..frame import Frame, OcvFrame, AnyFrame


class Source(Frame):
    """Basic source."""

    def __init__(self, src: Union[int, str, AnyFrame] = None):
        """

        :param src: Source id (int), path (str) or frame (np array)

        """
        frame = None

        if src is not None and not isinstance(src, (str, int)):
            frame, src = src, ''

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
