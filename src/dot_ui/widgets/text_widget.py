from .base_widget import *


class Text(Widget):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        alignment_x="center",
        alignment_y="center",
        typeface="",
        font_size=20,
        bold=False,
        italic=False,
    ):
        Widget.__init__(self, x = 0, y = 0, width = 100, height = 100)
