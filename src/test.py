import pygame
from dot_ui import Window, Widget

win = Window(title="Test")

win.print_fps = True


def move_with_mouse(self: Widget, delta):
    self.size[:] = pygame.mouse.get_pos()
    self.size[:] = self.size.target - self.pos[:]
    self.size.jump()

moves_with_mouse = Widget(160, 100, 100, 100)
moves_with_mouse.add_behaviour("tick", move_with_mouse)

win.floating_widgets.append(moves_with_mouse)
win.floating_widgets.append(Widget(50, 100, 100, 100))
win.open()
