from typing import Tuple, Union

from numpy.core.multiarray import ndarray

from .backend import cv
from .misc.colors import TypeColor, to_rgb


OcvFrame = ndarray
AnyFrame = Union[OcvFrame, 'Frame']


class Frame:
    """Represents a frame."""

    __slots__ = ['_frame']

    def __init__(self, frame: OcvFrame = None):
        self._frame = frame

    @property
    def frame(self) -> OcvFrame:
        return self._frame

    def _set_frame(self, frame: OcvFrame) -> 'Frame':
        self._frame = frame
        return self

    def fill(self, color: TypeColor):
        """Fills the canvas with the given color.

        :param color:

        """
        self.frame[:] = to_rgb(color)

    def resize(self, width: int, height: int) -> 'Frame':
        """Resizes the current frame inplace.

        :param width:
        :param height:

        """
        return self._set_frame(cv.resize(self.frame, (width, height)))

    def absdiff(self, frame: AnyFrame) -> 'Frame':
        """Returns absolute difference between
        the current and a given frame as a new Source.

        :param frame:

        """
        return Frame(cv.absdiff(self.frame, getattr(frame, 'frame', frame)))

    def make_gray(self) -> 'Frame':
        """Makes the current frame grayscale inplace."""
        return self._set_frame(cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY))

    def make_rgb(self) -> 'Frame':
        """Makes the current frame RGB inplace."""
        return self._set_frame(cv.cvtColor(self.frame, cv.COLOR_BGR2RGB))

    def canny(self, thr_1: int, thr_2: int) -> 'Frame':
        """Applies Canny Edge Detection algorithm
        to the current frame inplace.

        :param thr_1:
        :param thr_2:

        """
        return self._set_frame(cv.Canny(self.frame, thr_1, thr_2))

    def dilate(self, element: AnyFrame, iterations: int = None) -> 'Frame':
        """Dilates the current frame inplace.

        :param element:
        :param iterations:

        """
        return self._set_frame(cv.dilate(self.frame, getattr(element, 'frame', element), iterations=iterations))

    def blur(self, ksize: Tuple[int, int]) -> 'Frame':
        """Blures the current frame inplace.

        :param ksize: Kernel size tuple (width, height)

        """
        return self._set_frame(cv.blur(self.frame, ksize))