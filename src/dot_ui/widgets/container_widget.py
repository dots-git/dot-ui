from .base_widget import *


class Container(Widget):
    def __init__(self, x = 0, y = 0, width = 100, height = 100, floating = True):
        Widget.__init__(self, x, y, width, height)
        self._widget_grid: "list[list[Widget]]" = [[]]
        self._floating_widgets: "list[Widget]" = []
        self._floating = floating

    def add_widget(self, widget: Widget, x = None, y = None):
        widget.change_parent(self)
        if self._floating:
            self._floating_widgets.append(widget)
            if x is not None:
                widget.pos.x = x
            if y is not None:
                widget.pos.y = y
        else:
            self._widget_grid.append(widget)

    def remove_widget(self, widget):
        for w in self._widget_grid:
            if widget is w:
                self._widget_grid.remove(w)
        for w in self._floating_widgets:
            if widget is w:
                self._floating_widgets.remove(w)

    def set_grid_size(self, columns: int, rows: int):
        new_grid = [[None for _ in range(columns)] for _ in range(rows)]

    def _tick(self, delta):
        super()._tick(delta)
        for widget in self.child_list:
            widget._tick(delta)

    @property
    def floating(self):
        return self._floating
    
    @floating.setter
    def floating(self, value: bool):
        self._floating = value
        if self._floating:
            for column in self._widget_grid:
                for widget in column:
                    if widget is not None:
                        self._floating_widgets.append(widget)
            self._widget_grid = [[]]
        else:
            size = roof(sqrt(len(self._floating_widgets)))
            x = 0
            for widget in self._floating_widgets:
                if len(self._widget_grid[x]) < size:
                    self._widget_grid[x].append(widget)
                else:
                    self._widget_grid.append([])
                    x += 1
            self._floating_widgets = []
    
    @property
    def children(self):
        if self._floating:
            return self._floating_widgets
        else:
            return self._widget_grid
    
    @property
    def child_list(self):
        if self._floating:
            return self._floating_widgets
        else:
            return [w for w in [column for column in self._widget_grid] if w is not None]