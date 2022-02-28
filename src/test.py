from dot_ui import *

win = Window(title="Test")

# DotRenderer.set_shadow_offset(Vector2(13, 13))
# AnimVec.set_default_acceleration(2000)

# Input.add_action("Close", KeyCombination(Key.Q, Key.L_CTRL))
# Input.add_action("Up", Key.UP, Key.W)
# Input.add_action("Left", Key.LEFT, Key.A)
# Input.add_action("Down", Key.DOWN, Key.S)
# Input.add_action("Right", Key.RIGHT, Key.D)

# Key.set_repeat(200, 100)


# def move_with_mouse_and_keys(self: Widget, delta):
#     if Input.action_just_pressed("Close"):
#         self.close()

#     if Input.action_just_pressed("Up"):
#         self.pos -= Vector2(0, 100)
#     if Input.action_just_pressed("Down"):
#         self.pos += Vector2(0, 100)
#     if Input.action_just_pressed("Left"):
#         print("Moving left")
#         self.pos -= Vector2(100, 0)
#     if Input.action_just_pressed("Right"):
#         self.pos += Vector2(100, 0)

#     if any(Mouse.pressed):
#         self.pos = Mouse.pos

#     if Key.pressed[Key.L_SHIFT]:
#         # Jump to the target position (Effectively turns off animation)
#         self.pos.jump()


# def draggable_init(self: Widget):
#     self.being_moved = False


# def draggable(self: Widget, delta):
#     if Mouse.just_pressed_left:
#         if Mouse.pos.in_rect(self.transform):
#             self.being_moved = True
#     if Mouse.just_released_left:
#         self.being_moved = False

#     if self.being_moved:
#         self.pos += Mouse.movement


# moves_with_mouse_and_keys = Widget(100, 100, 100, 100)
# moves_with_mouse_and_keys.add_behaviour(
#     "Draggable", draggable, draggable_init
# )

# win.add_widget(moves_with_mouse_and_keys)
win.open()
