from typing import Union, Callable

from ...backend import cv

TypeNumber = Union[int, float]


class Trackbar:
    """Represents a trackbar."""

    def __init__(
            self,
            name,
            *,
            max: TypeNumber = None,
            default: TypeNumber = None,
            callback: Callable = None,
            step: TypeNumber = None,
            keys: str = None
    ):
        """

        :param name: Name to show in UI and address this in opencv api.
        :param max: Max value. Default: 100
        :param default: Default (current) value. Default: 0
        :param callback: Function to be called on trackbar value change through UI.
        :param step: Step to inc/dec trackbar value. Default: 1
        :param keys: Two-letter string to represent keys to inc and dec value.

        """
        self.name = name

        self._default = default or 0
        self._max = max or 100

        self.keys = {}

        if keys:
            assert len(keys) == 2, 'Trackbar `keys` param is expected to be 2 char length.'
            self.keys = {keys[0]: self.dec, keys[1]: self.inc}

        self.step = step or 1

        self.callback = callback or self.onChange
        self._window_name = None
        self._value = default

    def __float__(self):
        return float(self.value)

    def __index__(self):
        return int(self.value)

    def __int__(self):
        return int(self.value)

    def bind(self, window_name: str):
        """Binds the trackabr to the given window.

        :param window_name:

        """
        self._window_name = window_name
        cv.createTrackbar(self.name, window_name, self._default, self._max, self.callback)

    def inc(self):
        """Increments the current value."""
        self.value += self.step

    def dec(self):
        """Decrements the current value."""
        self.value -= self.step

    def get_value(self) -> TypeNumber:
        """Force getting current value."""
        return cv.getTrackbarPos(self.name, self._window_name)

    def _get_value(self) -> TypeNumber:
        return self._value or self._default

    def _set_value(self, val: TypeNumber):
        cv.setTrackbarPos(self.name, self._window_name, val)

    value = property(_get_value, _set_value)
    """Current trackbar value."""

    def onChange(self, val: TypeNumber):
        """Issued on value change from UI."""
        self._value = val
