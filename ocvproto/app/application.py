from pathlib import Path
from typing import Callable, Union, Optional, Tuple, List, Dict

from .config import Config
from .keys import Key
from ..backend import cv

TypeKey = Union[str, int]
TypeConfig = Optional[Union[str, Path]]


class Application:
    """Represents ocvproto application."""

    def __init__(self, *, config: TypeConfig = None):
        """

        :param config: Configuration to be used.

        """
        self._config: Optional[Config] = None
        self._key_map = {}
        self._loop_func = lambda: None
        self._hooks: Dict[str, List[Callable]] = {
            'config_save': [],
            'config_load': [],
        }
        self.set_config(config)

    def set_config(self, config: TypeConfig, keys: Tuple[TypeKey, TypeKey] = None):
        """Sets configuration from the app.

        :param config: Configuration object.
        :param keys: Keys tuple to save and load configuration.

        """
        if config is None:
            return

        config = Config(config)

        self._config = config
        self._bind_config_keys(keys)
        self.config_load()

    def _bind_config_keys(self, keys: Tuple[TypeKey, TypeKey] = None):
        bind = self.bind_key
        save, load = keys or ('s', 'r')
        bind(save, self.config_save)
        bind(load, self.config_load)

    def config_save(self):
        """Saves current configuration to config file."""
        config = self._config
        for hook in self._hooks['config_save']:
            hook(config)
        config.save()

    def config_load(self):
        """Loads a configuration from config file."""
        config = self._config
        config.load()

        for hook in self._hooks['config_load']:
            hook(config)

    def hook_register(self, key: str, func: Callable):
        """Registers a hook.

        :param key: Hooks group key.
        :param func: Hook function to add to group.

        """
        self._hooks[key].append(func)

    def bind_key(self, key: TypeKey, func: Callable):
        """Binds a key to a function.

        :param key:
        :param func:

        """
        if not isinstance(key, int):
            key = ord(key)

        self._key_map[key] = func

    def set_loop_func(self, func: Callable):
        """Sets a function to perform in a main app loop."""
        self._loop_func = func

    def loop(self):
        """Main application loop.
        Handles keys listening and issues a loop function (see .set_loop_func()).

        """
        esc = Key.ESC
        key_map = self._key_map
        func = self._loop_func

        wait = cv.waitKey

        while True:

            yield

            func()

            key = wait(5) & 0xff

            if key == esc:
                break

            key_handler = key_map.get(key)
            if key_handler:
                key_handler()
