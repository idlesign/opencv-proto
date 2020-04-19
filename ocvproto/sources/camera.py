from typing import Union

from .video import Video


class Camera(Video):
    """Represents a camera device."""

    def __init__(self, src: Union[int, str] = 0):
        """

        :param src: Device path (str) or id (int). Default 0.

            E.g.:
                * '/dev/video0'
                * 0
                * 1

        """
        super().__init__(src)
