from tkinter import W
from .base_widget import *


class Container(Widget):
    def __init__(self, x, y, width, height):
        Widget.__init__(self, x, y, width, height)
        self.widget_grid: "list[list[Widget]]" = []
        self.floating_widgets: "list[Widget]" = []

    def add_widget(self, widget, floating=True):
        if floating:
            self.floating_widgets.append(widget)
        else:
            self.widget_grid.append(widget)

    def _tick(self, delta):
        super()._tick(delta)
        for widget in self.floating_widgets:
            if widget._is_garbage:
                self.floating_widgets.remove(widget)
        for widget in self.floating_widgets:
            widget._tick(delta)
