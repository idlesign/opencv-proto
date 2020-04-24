from typing import Union

from .video import Video, Property
from ..backend import cv


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

    brightness = Property(cv.CAP_PROP_BRIGHTNESS)
    contrast = Property(cv.CAP_PROP_CONTRAST)
    saturation = Property(cv.CAP_PROP_SATURATION)
    hue = Property(cv.CAP_PROP_HUE)
    gain = Property(cv.CAP_PROP_GAIN)
    exposure = Property(cv.CAP_PROP_EXPOSURE)
