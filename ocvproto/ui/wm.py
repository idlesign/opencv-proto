from typing import List, Generator, Tuple

from .window import Window, Trackbar
from ..app import Application, Config
from ..backend import cv
from ..sources.base import TypeFrame


class WindowManager:
    """Manages windows."""

    def __init__(self, windows: List[Window] = None, app: Application = None):
        """

        :param windows: Windows to manage. If not set,
            one window is automatically constructed.

        :param app: ocvproto application object. Automatically constructed if not set.

        """
        if app is None:
            app = Application()

        self.app = app

        if not windows:
            windows = [Window()]

        self._windows = windows

        self._bind_trackbar_keys()
        app.set_loop_func(self.render)
        self._hooks_bind()

    def _hooks_bind(self):
        app = self.app
        app.hook_register('config_save', self.config_update)
        app.hook_register('config_load', self.config_load)

    @property
    def window(self) -> Window:
        """Default window."""
        return self._windows[0]

    def config_update(self, config: Config):
        """Updates data gathered from managed windows in the given config.

        :param config:

        """
        data = {}

        for window, trackbar in self.iter_trackbars():
            window_data = data.setdefault(window.name, {'trackvals': {}})
            window_data['trackvals'][trackbar.name] = trackbar.value

        config.set_data('windows', data)

    def config_load(self, config: Config):
        """Updates managed windows using data from the given config.

        :param config:

        """
        windows_data: dict = config.get_data('windows', {})

        for window, trackbar in self.iter_trackbars():
            window_data = windows_data.get(window.name)

            if window_data:
                trackbar_vals = window_data.get('trackvals')
                if trackbar_vals:
                    trackbar_val = trackbar_vals.get(trackbar.name)
                    if trackbar_val is not None:
                        trackbar.value = trackbar_val

    def iter_trackbars(self) -> Generator[Tuple[Window, Trackbar], None, None]:
        """Generator yielding managed windows and trackbars."""
        for window in self._windows:
            for trackbar in window.trackbars.values():
                yield window, trackbar

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        cv.destroyAllWindows()

    def set_frame(self, frame: TypeFrame):
        """Sets frame to be rendered in default window.

        :param frame:

        """
        self.window.set_frame(frame)

    def render(self):
        """Renders managed windows."""
        for window in self._windows:
            window.render()

    def _bind_trackbar_keys(self):

        bind = self.app.bind_key

        for window, trackbar in self.iter_trackbars():
            for key, func in trackbar.keys.items():
                bind(key, func)
