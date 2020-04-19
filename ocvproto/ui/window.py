from functools import reduce
from operator import ior
from typing import Union, Dict, List

from .trackbar import Trackbar
from ..backend import cv

WIN_COUNT = 0


class Window:

    def __init__(self, name=None):

        if not name:
            global WIN_COUNT
            WIN_COUNT += 1
            # Not a uuid to be friendly to Config save/load.
            name = f'{WIN_COUNT}'

        self.name = name
        self.trackbars = {}
        self.create()
        self._frame = None

    def create(self, *, autosize=True):

        flags = [
            cv.WINDOW_AUTOSIZE if autosize else cv.WINDOW_NORMAL,
            cv.WINDOW_KEEPRATIO
        ]

        cv.namedWindow(self.name, reduce(ior, flags))

    def position(self, *, x, y):
        cv.moveWindow(self.name, x, y)

    def resize(self, *, width, height):
        cv.resizeWindow(self.name, width, height)

    def add_trackbar(self, *trackbars):
        for trackbar in trackbars:
            self.trackbars[trackbar.name] = trackbar
            trackbar.bind(self.name)
        return self

    def add_trackbar_group(
            self,
            definitions: Union[int, Dict[str, dict], List[dict], List[str]],
            prefix='',
            **common_kwargs
    ):
        trackbars = []

        if prefix:
            prefix = f'{prefix} '

        if isinstance(definitions, int):
            # Just a number of trackbars to generate.
            definitions = {f'{idx+1}': {} for idx in range(definitions)}

        elif isinstance(definitions, list):
            definitions_ = {}

            for idx, definition in enumerate(definitions, 1):
                if isinstance(definition, dict):
                    # A list of params. Generate names
                    definitions_[f'{idx}'] = definition
                else:
                    # A list of names. Generate params.
                    definitions_[definition] = {}

            definitions = definitions_

        for title, definition in definitions.items():
            definition = definition or {}

            kwargs = {
                'keys': definition.get('keys')
            }

            trackbar = Trackbar(
                f'{prefix}{title}',
                **{**common_kwargs, **kwargs}
            )
            trackbars.append(trackbar)
            self.add_trackbar(trackbar)

        return tuple(trackbars)

    def set_frame(self, frame):
        self._frame = frame

    def render(self):
        frame = self._frame
        if frame is not None:
            cv.imshow(self.name, frame)
