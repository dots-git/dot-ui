from dot_ui import Window, Widget, Container, Mouse, DotRenderer, Vector2

win = Window(title="Test")

DotRenderer.set_corner_radius(10)
DotRenderer.set_shadow_radius(20)
DotRenderer.set_shadow_offset(Vector2(7, 7))

win.print_fps = True


def move_with_mouse(self: Widget, delta):
    new_size = Mouse.pos - self.pos
    self.size = new_size


container = Container(10, 10, 700, 400)


moves_with_mouse = Widget(10, 10, 100, 100)
moves_with_mouse.add_behaviour("tick", move_with_mouse)

container.add_widget(moves_with_mouse)

win.floating_widgets.append(moves_with_mouse)
win.open()
