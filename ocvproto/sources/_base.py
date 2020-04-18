from typing import Tuple

import cv2 as cv


class Source:

    def __init__(self, src=None):

        frame = None

        if src is not None and not isinstance(src, str):
            frame, src = src, ''

        self._src = src or ''
        self._frame = frame

    def _set_frame(self, frame):
        self._frame = frame
        return self

    @property
    def frame(self):
        frame = self._frame

        if frame is None:
            frame = self.read()

        return frame

    def read(self):  # pragma: nocover
        raise NotImplementedError

    ######

    def resize(self, width, height):
        return self._set_frame(cv.resize(self.frame, (width, height)))

    def absdiff(self, frame) -> 'Source':
        return Source(cv.absdiff(self.frame, frame))

    def make_gray(self):
        return self._set_frame(cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY))

    def make_rgb(self):
        return self._set_frame(cv.cvtColor(self.frame, cv.COLOR_BGR2RGB))

    def canny(self, thr_1, thr_2):
        return self._set_frame(cv.Canny(self.frame, thr_1, thr_2))

    def dilate(self, element, iterations=None):
        return self._set_frame(cv.dilate(self.frame, element, iterations=iterations))

    def blur(self, ksize: Tuple[int, int]):
        return self._set_frame(cv.blur(self.frame, ksize))
