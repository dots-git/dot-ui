from typing import Iterable
import numpy as np


def iterable_to_array(iterable: Iterable) -> np.ndarray:
    list = []
    for item in iterable:
        list.append(item)
    return np.asarray(list)

def roof(x: float) -> int:
    return int(x if x % 1 == 0 else x + 1)

def floor(x: float) -> int:
    return int(x)