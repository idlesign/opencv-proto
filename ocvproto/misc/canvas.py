from .colors import TypeColor
from ..backend import np
from ..frame import Frame


class Canvas(Frame):
    """Represents a canvas."""

    __slots__ = ['_frame']

    def __init__(self, width: int = 640, height: int = 480, *, channels: int = 3, color: TypeColor = None):
        """

        :param width:
        :param height:
        :param channels:
        :param color:

        """
        super().__init__(np.zeros((height, width, channels), np.uint8))

        if color:
            self.fill(color)
