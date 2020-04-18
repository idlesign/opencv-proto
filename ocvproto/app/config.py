import json
from pathlib import Path
from typing import Optional, Union, Any


class Config:

    def __init__(self, fpath: Optional[Union[str, Path]]):
        self._fpath = Path(fpath)
        self._data = {
            'metadata': {},
            'data': {},
        }

    def set_data(self, key: str, value: Any):
        self._data['data'][key] = value

    def get_data(self, key: str, default: Any = None):
        return self._data['data'].get(key, default)

    def save(self):
        fpath = self._fpath

        if not fpath:
            return

        with open(str(fpath), 'w') as f:
            f.write(json.dumps(self._data))

    def load(self):
        fpath = self._fpath

        if not (fpath and fpath.exists()):
            return

        with open(f'{fpath}') as f:
            self._data = json.loads(f.read())
