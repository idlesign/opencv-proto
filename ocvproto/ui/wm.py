from typing import List, Generator, Tuple

from .window import Window, Trackbar
from ..app import Application, Config
from ..backend import cv


class WindowManager:

    def __init__(self, windows: List[Window] = None, app: Application = None):

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
        app.hook_register('config_save', self.config_save)
        app.hook_register('config_load', self.config_load)

    def config_save(self, config: Config):

        data = {}

        for window, trackbar in self.iter_trackbars():
            window_data = data.setdefault(window.name, {'trackvals': {}})
            window_data['trackvals'][trackbar.name] = trackbar.value

        config.set_data('windows', data)

    def config_load(self, config: Config):
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
        for window in self._windows:
            for trackbar in window.trackbars.values():
                yield window, trackbar

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        cv.destroyAllWindows()

    def set_frame(self, frame):
        self._windows[0].set_frame(frame)

    def render(self):
        for window in self._windows:
            window.render()

    def _bind_trackbar_keys(self):

        bind = self.app.bind_key

        for window, trackbar in self.iter_trackbars():
            for key, func in trackbar.keys.items():
                bind(key, func)
