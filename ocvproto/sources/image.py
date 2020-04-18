import cv2 as cv

from ._base import Source
from ..exceptions import SourceError


class Image(Source):

    def read(self):
        frame = cv.imread(self._src)

        if frame is None:
            raise SourceError(f"Unable to load image '{self._src}'.")

        self._frame = frame

        return frame
