from .base import Source, TypeFrame
from ..backend import cv
from ..exceptions import SourceError


class Image(Source):
    """Represents an image."""

    def read(self) -> TypeFrame:
        frame = cv.imread(self._src)

        if frame is None:
            raise SourceError(f"Unable to load image '{self._src}'.")

        self._frame = frame

        return frame
