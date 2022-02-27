from .base_widget import *


class Text(Widget):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        Text,
        alignment_x="center",
        alignment_y="center",
        typeface="",
        font_size=20,
        bold=False,
        italic=False,
    ):
        Widget.__init__(self, x, y, width, height)
        self.has_shadow = False
