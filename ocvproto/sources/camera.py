from typing import Union

from .video import Video


class Camera(Video):
    """Camera device."""

    def __init__(self, src: Union[int, str] = 0):
        """

        :param src: Device path or id. Default 0.

            E.g.:
                * '/dev/video0'
                * 0
                * 1

        """
        super().__init__(src)
