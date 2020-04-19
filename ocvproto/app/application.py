from pathlib import Path
from typing import Callable, Union, Optional, Tuple, List, Dict

from .config import Config
from .keys import Key
from ..backend import cv

TypeKey = Union[str, int]
TypeConfig = Optional[Union[str, Path]]


class Application:

    def __init__(self, *, config: TypeConfig = None):
        self._config: Optional[Config] = None
        self._key_map = {}
        self._loop_func = lambda: None
        self._hooks: Dict[str, List[Callable]] = {
            'config_save': [],
            'config_load': [],
        }
        self.set_config(config)

    def set_config(self, config: TypeConfig, keys: Tuple[TypeKey, TypeKey] = None):

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
        config = self._config
        for hook in self._hooks['config_save']:
            hook(config)
        config.save()

    def config_load(self):
        config = self._config
        config.load()

        for hook in self._hooks['config_load']:
            hook(config)

    def hook_register(self, key: str, func: Callable):
        self._hooks[key].append(func)

    def set_loop_func(self, func: Callable):
        self._loop_func = func

    def bind_key(self, key: TypeKey, func: Callable):

        if not isinstance(key, int):
            key = ord(key)

        self._key_map[key] = func

    def loop(self):

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
