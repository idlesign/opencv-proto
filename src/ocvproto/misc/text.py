from .colors import to_rgb, TypeColor
from ..backend import cv
from ..frame import TypePoint
from ..sources.base import AnyFrame


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
            pos: TypePoint = None,
            weight: int = None
    ):
        """

        :param val: Text value itself.
        :param face: Font face alias (see .face_map keys). Default: normal
        :param scale: Scale factor. Default: 1
        :param color: Color RGB tuple or alias (see `COLORS`). Default: white
        :param pos: Position tuple (x, y) in frame from top-left. Default: (20, 20)
        :param weight: Line thickness. Default: 1

        """
        self._val = val or ''
        self._face = self.face_map.get(face, self.face_map['normal'])
        self._scale = scale or 1
        self._color = to_rgb(color or 'white')
        self._weight = weight or 1
        self._pos = pos or (20, 20)

    @classmethod
    def put_on_demo(cls, frame: AnyFrame, text: str = 'Test Text 1 2 3 4 5'):
        """Demonstrates available font faces applying all of them to the frame.

        :param frame: Frame to apply text to.
        :param text: Text value to on frame.

        """
        for idx, face in enumerate(Text.face_map, 1):
            cls(f'{face}: {text}', face=face, pos=(20, idx * 35)).put_on(frame)

    def put_on(self, frame: AnyFrame, text: str = None, *, pos: TypePoint = None):
        """Applies text to the frame.

        :param frame: Frame to apply text to.
        :param text: Text value to set on frame. If not set, value from initializer is used.
        :param pos: Position tuple (x, y) in frame from top-left. Default: (20, 20)

        """
        cv.putText(
            getattr(frame, 'frame', frame),
            text or self._val,
            pos or self._pos,
            self._face,
            self._scale,
            self._color,
            self._weight
        )
