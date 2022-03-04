from dot_ui import *


DotRenderer._corner_radius = 0


def print_fps(self: Widget, delta: float):
    print(1 / delta)


Window(
    b_print=print_fps
).open()
