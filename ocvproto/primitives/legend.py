from typing import Sequence, Dict

try:
    from colorhash import ColorHash

except ImportError:
    raise ImportError('Legend requires `colorhash` library: pip install colorhash')

from ..frame import Frame, TypePoint
from ..misc.text import Text
from ..misc.colors import TypeRgb


class Legend:
    """Represents a color-legend for labels."""

    def __init__(
            self,
            labels: Sequence[str],
            pos: TypePoint = None,
            width: int = None,
            gap: int = None
    ):
        """

        :param labels: Strings to get colors for.
        :param pos: Position (x, y) to place top left legend corner. Default: (20, 20)
        :param width: Default: 250
        :param gap: Base gap (also a height for each color stripe). Default: 25

        """
        self.labels: Dict[str, TypeRgb] = {label: ColorHash(label).rgb for label in labels}
        self._gap = gap or 25
        self._pos = pos or (20, 20)
        self._width = width or 250

    def put_on(self, frame: Frame, *, pos: TypePoint = None):
        """Applies the legend to the frame.

        :param frame: Frame to apply the legend to.
        :param pos: Position (x, y) to place top left legend corner. Default: (20, 20)

        """
        gap = self._gap
        width = self._width
        pos = pos or self._pos

        text_left, text_top = pos

        for idx, (label, color) in enumerate(self.labels.items()):
            step = (idx * gap) + text_top

            frame.draw_rectangle(
                pos=(text_left, step),
                width=width,
                height=gap,
                color=color,
            )

            # todo remove +17 hardcoded for the given text scale
            Text(label, scale=0.5, pos=(text_left + 5, step + 17)).put_on(frame)
