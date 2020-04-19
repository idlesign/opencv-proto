from functools import reduce
from operator import ior
from typing import Union, Dict, List, Tuple

from .trackbars import Trackbar
from ..backend import cv
from ..sources.base import TypeFrame

WIN_COUNT = 0


class Window:
    """Represents a window."""

    def __init__(self, name: str = None):
        """

        :param name: Window name. If not set, automatically generated.

        """
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
        """Creates a window.

        :param autosize: If try, window is automatically
            sized to a content.

        """
        flags = [
            cv.WINDOW_AUTOSIZE if autosize else cv.WINDOW_NORMAL,
            cv.WINDOW_KEEPRATIO
        ]

        cv.namedWindow(self.name, reduce(ior, flags))

    def position(self, *, x: int, y: int):
        """Positions the window."""
        cv.moveWindow(self.name, x, y)

    def resize(self, *, width: int, height: int):
        """Resizes the window.

        :param width:
        :param height:

        """
        cv.resizeWindow(self.name, width, height)

    def add_trackbar(self, *trackbars):
        """Add the given trackbars to the window.

        :param trackbars:

        """
        for trackbar in trackbars:
            self.trackbars[trackbar.name] = trackbar
            trackbar.bind(self.name)
        return self

    def add_trackbar_group(
            self,
            definitions: Union[int, Dict[str, dict], List[dict], List[str]],
            prefix: str = '',
            **common_kwargs
    ) -> Tuple:  # not Tuple[Trackbar, ...] to satisfy typechecker, when passing trackbar as param to ocv functions.
        """A shortcut to batch create trackbars in a declarative way.

        :param definitions: Definitions to construct trackbars.

            * Integer:
                * 2 - create two trackbars with generated titles and default params.

            * List:
                * ['one', 'two', 'three'] -
                    - create 3 trackbars with the given titles and default params.

                * [{'keys': 'kl'}, {}] -
                    - create 2 trackbars with generated titles and default params.

            * Dictionary:
                *   {'y': {'keys': 'kl'}, 'x': {'step': 20}}
                    - create 2 trackbars with the given titles and params.


        :param prefix: Prefix to add to trackbars titles.

        :param common_kwargs: Common keyword arguments to pass to all trackbars.

        """
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

    def set_frame(self, frame: TypeFrame):
        """Sets current frame for the window.

        :param frame:

        """
        self._frame = frame

    def render(self):
        """Renders window contents."""
        frame = self._frame
        if frame is not None:
            cv.imshow(self.name, frame)
