from typing import Callable


class Behaviour:
    def __init__(self, type: str, function: Callable):
        self.trigger = type
        self.function = function
