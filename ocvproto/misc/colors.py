from typing import Union, Tuple

TypeColor = Union[int, str, Tuple[int, int, int]]

COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
}
"""Color aliases to RGB tuples map."""


def to_rgb(value: TypeColor) -> Tuple[int, int, int]:
    """Translates the given color value to RGB tuple.

    :param value:

    """
    if isinstance(value, tuple):
        return value

    if isinstance(value, int):
        value = (value, value, value)

    elif isinstance(value, str):
        value = COLORS[value]

    return value
