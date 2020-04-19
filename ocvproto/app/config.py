import json
from pathlib import Path
from typing import Optional, Union, Any


class Config:
    """Represent an interface to configuration file."""

    def __init__(self, fpath: Optional[Union[str, Path]]):
        """

        :param fpath: Configuration file path.

        """
        self._fpath = Path(fpath)
        self._data = {
            'metadata': {},
            'data': {},
        }

    def set_data(self, key: str, value: Any):
        """Places the data into config section denoted by key.

        :param key:
        :param value:

        """
        self._data['data'][key] = value

    def get_data(self, key: str, default: Any = None):
        """Reads data from a config section denoted by key.

        :param key:
        :param default: Default values to return.

        """
        return self._data['data'].get(key, default)

    def save(self):
        """Saves configuration to file."""
        fpath = self._fpath

        if not fpath:
            return

        with open(str(fpath), 'w') as f:
            f.write(json.dumps(self._data))

    def load(self):
        """Loads configuration from file."""
        fpath = self._fpath

        if not (fpath and fpath.exists()):
            return

        with open(f'{fpath}') as f:
            self._data = json.loads(f.read())
