from .base import Source
from ..backend import cv
from ..exceptions import SourceError


class Image(Source):
    """Represents an image."""

    def read(self) -> 'Image':
        frame = cv.imread(self._src)

        if frame is None:
            raise SourceError(f"Unable to load image '{self._src}'.")

        return self._set_frame(frame)
