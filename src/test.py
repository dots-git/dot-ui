from dot_ui import *

DotRenderer.set_corner_radius(0)
DotRenderer.set_shadow_offset(Vector2(-2, -2))
DotRenderer.set_shadow_radius(10)
DotRenderer.set_default_color(Color.GREEN)


win = Window(title="Demo")

widget = Widget(10, 10)

win.add_widget(widget)

win.open()