import cv2 as cv


class Trackbar:

    def __init__(self, name, *, max=None, default=None, callback=None, step=None, keys=None):
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

    def bind(self, window_name):
        self._window_name = window_name
        cv.createTrackbar(self.name, window_name, self._default, self._max, self.callback)

    def inc(self):
        self.value += self.step

    def dec(self):
        self.value -= self.step

    def get_value(self):
        return cv.getTrackbarPos(self.name, self._window_name)

    def _get_value(self):
        return self._value

    def _set_value(self, val):
        cv.setTrackbarPos(self.name, self._window_name, val)

    value = property(_get_value, _set_value)

    def onChange(self, val):
        self._value = val
