from ..backend import np
from .colors import to_rgb, TypeColor


class Canvas:
    """Represents a canvas."""

    __slots__ = ['frame']

    def __init__(self, width: int = 640, height: int = 480, *, channels: int = 3, color: TypeColor = None):
        """

        :param width:
        :param height:
        :param channels:
        :param color:

        """
        self.frame = np.zeros((height, width, channels), np.uint8)
        if color:
            self.fill(color)

    def fill(self, color: TypeColor):
        """Fills the canvas with the given color.

        :param color:

        """
        self.frame[:] = to_rgb(color)
