from typing import Tuple

from .colors import to_rgb, TypeColor
from ..backend import cv
from ..sources.base import TypeFrame


class Text:
    """Represents a text that can be placed into a frame."""

    # | FONT_ITALIC
    face_map = {
        'small': cv.FONT_HERSHEY_PLAIN,
        'normal': cv.FONT_HERSHEY_SIMPLEX,
        'duplex': cv.FONT_HERSHEY_DUPLEX,
        'triplex': cv.FONT_HERSHEY_TRIPLEX,
        'complex': cv.FONT_HERSHEY_COMPLEX,
        'complex-sm': cv.FONT_HERSHEY_COMPLEX_SMALL,
        'hand': cv.FONT_HERSHEY_SCRIPT_SIMPLEX,
        'hand-complex': cv.FONT_HERSHEY_SCRIPT_COMPLEX,
    }

    def __init__(
            self,
            val: str = None,
            *,
            face: str = None,
            scale: float = None,
            color: TypeColor = None,
            pos: Tuple[int, int] = None
    ):
        """

        :param val: Text value itself.
        :param face: Font face alias (see .face_map keys). Default: normal
        :param scale: Scale factor. Default: 1
        :param color: Color RGB tuple or alias (see `COLORS`). Default: white
        :param pos: Position tuple (x, y) in frame from top-left. Default: (20, 20)

        """
        self.val = val or ''
        self.face = self.face_map.get(face, self.face_map['normal'])
        self.scale = scale or 1
        self.color = to_rgb(color or 'white')
        self.line = 4  # 4, 8, CV_AA
        self.pos = pos or (20, 20)

    @classmethod
    def apply_demo(cls, frame: TypeFrame, text: str = 'Test Text 1 2 3 4 5'):
        """Demonstrates available font faces applying all the to a frame.

        :param frame: Frame to apply text to.
        :param text: Text value to on frame.

        """
        for idx, face in enumerate(Text.face_map, 1):
            cls(f'{face}: {text}', face=face, pos=(20, idx * 35)).apply(frame)

    def apply(self, frame, text: str = None, *, pos: Tuple[int, int] = None):
        """

        :param frame: Frame to apply text to.
        :param text: Text value to set on frame. If not set, value from initializer is used.
        :param pos: Position tuple (x, y) in frame from top-left. Default: (20, 20)

        """
        cv.putText(frame, text or self.val, pos or self.pos, self.face, self.scale, self.color, self.line)
