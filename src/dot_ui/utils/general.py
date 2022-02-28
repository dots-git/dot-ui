from typing import Iterable
import numpy as np


def iterable_to_array(iterable: Iterable) -> np.ndarray:
    list = []
    for item in iterable:
        list.append(item)
    return np.asarray(list)
