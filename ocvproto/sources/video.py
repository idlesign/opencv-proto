from functools import partial
from pathlib import Path
from typing import Union, Dict, Any

from .base import Source, OcvFrame
from .image import Image
from ..backend import cv
from ..exceptions import SourceError
from ..frame import AnyFrame


class Property:
    """Represents a capture video property with restrictions."""

    def __init__(self, cv_prop: int, *, max: int = None):
        self._cv_prop = cv_prop
        self.max = max

    def __get__(self, instance, cls):
        return instance._cap.get(self._cv_prop)

    def __set__(self, instance, value):
        instance._cap.set(self._cv_prop, value)


class Video(Source):
    """Represents a video."""

    def __init__(self, src: Union[str, OcvFrame]):
        super().__init__(src)
        self._cap = None
        self._writer = None

    def __enter__(self) -> 'Video':
        self._cap = cv.VideoCapture(self._src)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cap.release()

        writer = self._writer

        if writer is not None:
            writer.release()

    def get_image(self) -> Image:
        """Returns image object from the current frame."""
        return Image(self.frame)

    def dump_image(self, fpath: Union[str, Path] = None):
        """Dumps the image into a file.

        :param fpath: Filepath to store image into.
            If not set, name is generated automatically.

        """
        self.get_image().dump(fpath)

    sharpness = Property(cv.CAP_PROP_SHARPNESS)
    gamma = Property(cv.CAP_PROP_GAMMA)
    focus = Property(cv.CAP_PROP_FOCUS)
    zoom = Property(cv.CAP_PROP_ZOOM)
    width = Property(cv.CAP_PROP_FRAME_WIDTH, max=4096)
    height = Property(cv.CAP_PROP_FRAME_HEIGHT, max=3072)
    fps = Property(cv.CAP_PROP_FPS, max=60)

    @property
    def codec(self) -> str:
        """FOURCC codec alias."""
        val = int(self._cap.get(cv.CAP_PROP_FOURCC))
        return ''.join([chr((val >> 8 * i) & 0xFF) for i in range(4)])

    def set_property(self, name: str, value: int):
        """Helper method to set property value.

        :param name: Property name.
        :param value:

        """
        setattr(self, name, value)

    def describe_properties(self) -> Dict[str, Any]:
        """Returns descriptions for CV properties found
        in the class of this object and its bases.

        One can initialize trackbars with these descriptions:
        see Window.add_trackbar_group()

        """
        properties = {}

        cls = self.__class__
        for cls in [cls] + list(cls.__bases__):

            for attr, val in cls.__dict__.items():

                if isinstance(val, Property):
                    properties[attr] = {
                        'default': getattr(self, attr),
                        'callback': partial(self.set_property, attr),
                        'max': val.max
                    }

        return properties

    def dump_setup(
            self,
            fpath: Union[str, Path] = 'ocvproto.avi',
            *,
            width: int = None,
            height: int = None,
            fps: Union[int, float] = None,
            codec: str = 'XVID',
    ) -> cv.VideoWriter:
        """Configures write parameters.
        Returns opencv writer object.

        :param fpath: Filepath.
        :param width:
        :param height:
        :param fps: Frames per second.
        :param codec: FOURCC codec alias.

        """
        if codec is None:
            codec = self.codec

        fcc = cv.VideoWriter_fourcc(*codec)

        writer = cv.VideoWriter(
            f'{fpath}',
            fcc,
            fps or self.fps,
            (width or self.width, height or self.height)
        )
        self._writer = writer
        return writer

    def dump(self, frame: AnyFrame = None):
        """Writes the current or the given frame.
        Automatically configures writer object is needed.

        """
        if frame is None:
            frame = self.frame

        else:
            frame = getattr(frame, 'frame', frame)

        writer = self._writer
        if writer is None:
            writer = self.dump_setup()

        writer.write(frame)

    def read(self) -> 'Video':
        success, frame = self._cap.read()

        if not success:
            raise SourceError(f"Unable to read from '{self._src}'.")

        return self._set_frame(frame)
