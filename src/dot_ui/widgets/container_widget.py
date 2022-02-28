from .base_widget import *


class Container(Widget):
    def __init__(self, x = 0, y = 0, width = 100, height = 100):
        Widget.__init__(self, x, y, width, height)
        self.widget_grid: "list[list[Widget]]" = []
        self.floating_widgets: "list[Widget]" = []

    def add_widget(self, widget: Widget, floating=True):
        widget.change_parent(self)
        if floating:
            self.floating_widgets.append(widget)
        else:
            self.widget_grid.append(widget)

    def remove_widget(self, widget):
        for w in self.widget_grid:
            if widget is w:
                self.widget_grid.remove(w)
        for w in self.floating_widgets:
            if widget is w:
                self.floating_widgets.remove(w)

    def _tick(self, delta):
        super()._tick(delta)
        for widget in self.floating_widgets + self.widget_grid:
            widget._tick(delta)
