from .base_widget import *

class Container(Widget):
    def __init__(self, x, y, width, height):
        Widget.__init__(self, x, y, width, height)
        self.widget_grid: 'list[list[Widget]]' = []
        self.floating_widgets: 'list[Widget]' = []