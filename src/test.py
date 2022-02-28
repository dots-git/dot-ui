from dot_ui import *

DotRenderer.set_shadow_radius(100)

win = Window(title="Demo")

win.print_fps = True

def movable_init(self: Widget):
    self.moving = False

def movable(self: Widget, delta: float):
    if Mouse.just_pressed_left and Mouse.pos.in_rect(self.transform):
        self.moving = True
    elif Mouse.just_released_left:
        self.moving = False

    if self.moving:
        self.pos += Mouse.movement

wid = Widget()
wid.add_behaviour("Movable", movable, movable_init)
win.add_widget(wid)

win.open()
