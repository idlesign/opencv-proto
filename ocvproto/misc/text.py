from typing import Tuple, Union

from .colors import COLORS
from ..backend import cv

TypeColor = Union[str, Tuple[int, int , int]]


class Text:

    # | FONT_ITALIC
    _face_map = {
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
        self.val = val or ''
        self.face = self._face_map.get(face, self._face_map['normal'])
        self.scale = scale or 1
        self.color = self._get_color(color or 'white')
        self.line = 4  # 4, 8, CV_AA
        self.pos = pos or (20, 20)

    def _get_color(self, value: TypeColor):
        if isinstance(value, str):
            value = COLORS[value]
        return value

    @classmethod
    def apply_demo(cls, frame, text: str = 'Test Text 1 2 3 4 5'):
        for idx, face in enumerate(Text._face_map, 1):
            cls(f'{face}: {text}', face=face, pos=(20, idx * 35)).apply(frame)

    def apply(self, frame, text: str = None, *, pos: Tuple[int, int] = None):
        cv.putText(frame, text or self.val, pos or self.pos, self.face, self.scale, self.color, self.line)
