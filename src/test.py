from dot_ui import *

win = Window(title="Test")

win.print_fps = True

def move_with_mouse(self: Widget, delta):
    self.size = Mouse.pos - self.pos
    if Input.action_just_released('Close'):
        self.remove()

moves_with_mouse = Widget(100, 100, 100, 100)
moves_with_mouse.add_behaviour('tick', move_with_mouse)

Input.add_action('Close', KeyCombination(Key.q, Key.l_ctrl))

win.floating_widgets.append(moves_with_mouse)
win.open()
