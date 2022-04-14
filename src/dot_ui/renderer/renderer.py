from pygame import Surface
from ..utils.draw import rect


class Renderer:
    '''
    Class for rendering widgets. Requires a drawing function for every widget type.
    '''
    configs = {}

    rendering_functions = {}

    @staticmethod
    def draw(widget):
        '''
        Draws a widget.
        '''

        # Check if the widget is actually part of the widget class.
        if not isinstance(widget, Widget):
            raise TypeError(f"{widget} is not a Widget.")

        # Find the correct function for drawing the widget based on the class name.
        # If no function is found, resort to the inherited class and keep going up the inheritance tree.

        # Get the class of the widget.
        widget_class = widget.__class__

        while widget_class.__name__ not in Renderer.rendering_functions:
            widget_class = widget_class.__bases__[0]
        
        # Call the function.
        Renderer.rendering_functions[widget_class.__name__](widget)

    @staticmethod
    def draw_widget(widget: Widget, surface: Surface):
        '''
        Draws a default widget
        '''
        x = widget.x
        y = widget.y
        width = widget.width
        height = widget.height
        try:
            fill_color = widget.fill_color
        except AttributeError:
            fill_color = None
        try:
            stroke_color = widget.stroke_color
        except AttributeError:
            stroke_color = None
        try:
            stroke_width = widget.stroke_width
        except AttributeError:
            stroke_width = None

        rect(
            widget.x,
            widget.y,
            widget.width,
            widget.height,
            widget.fill_color,
            widget.stroke_color,
            widget.stroke_width,
        )


Renderer.rendering_functions = {
    'Widget': Renderer.draw_widget,
    'Button': Renderer.draw_button,
    'Label': Renderer.draw_label,
    'List': Renderer.draw_list,
}