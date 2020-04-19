from typing import Tuple, Union

from numpy.core.multiarray import ndarray

from ..backend import cv

TypeFrame = ndarray


class Source:
    """Basic source."""

    def __init__(self, src: Union[int, str, TypeFrame] = None):
        """

        :param src: Source id (int), path (str) or frame (np array)

        """
        frame = None

        if src is not None and not isinstance(src, (str, int)):
            frame, src = src, ''

        if src is not 0:
            src = src or ''

        self._src = src
        self._frame = frame

    def _set_frame(self, frame: TypeFrame) -> 'Source':
        self._frame = frame
        return self

    @property
    def frame(self) -> TypeFrame:
        """Current frame."""
        frame = self._frame

        if frame is None:
            frame = self.read()

        return frame

    def read(self) -> TypeFrame:  # pragma: nocover
        """Read and return current frame."""
        raise NotImplementedError

    ######

    def resize(self, width: int, height: int) -> 'Source':
        """Resizes the current frame inplace.

        :param width:
        :param height:

        """
        return self._set_frame(cv.resize(self.frame, (width, height)))

    def absdiff(self, frame: TypeFrame) -> 'Source':
        """Returns absolute difference between
        the current and a given frame as a new Source.

        :param frame:

        """
        return Source(cv.absdiff(self.frame, frame))

    def make_gray(self) -> 'Source':
        """Makes the current frame grayscale inplace."""
        return self._set_frame(cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY))

    def make_rgb(self) -> 'Source':
        """Makes the current frame RGB inplace."""
        return self._set_frame(cv.cvtColor(self.frame, cv.COLOR_BGR2RGB))

    def canny(self, thr_1: int, thr_2: int) -> 'Source':
        """Applies Canny Edge Detection algorithm
        to the current frame inplace.

        :param thr_1:
        :param thr_2:

        """
        return self._set_frame(cv.Canny(self.frame, thr_1, thr_2))

    def dilate(self, element: ndarray, iterations: int = None) -> 'Source':
        """Dilates the current frame inplace.

        :param element:
        :param iterations:

        """
        return self._set_frame(cv.dilate(self.frame, element, iterations=iterations))

    def blur(self, ksize: Tuple[int, int]) -> 'Source':
        """Blures the current frame inplace.

        :param ksize: Kernel size tuple (width, height)

        """
        return self._set_frame(cv.blur(self.frame, ksize))
