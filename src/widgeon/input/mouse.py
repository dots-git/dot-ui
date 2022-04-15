import pygame
import numpy as np
from ..utils.vectors import Vector2


class Mouse:
    pressed = np.array([])
    pressed_left = False
    pressed_middle = False
    pressed_right = False

    just_pressed = pressed.copy()
    just_pressed_left = False
    just_pressed_middle = False
    just_pressed_right = False

    just_released = pressed.copy()
    just_released_left = False
    just_released_middle = False
    just_released_right = False

    _pressed_last_tick = pressed.copy()
    _pressed_left_last_tick = False
    _pressed_middle_last_tick = False
    _pressed_right_last_tick = False

    scroll_dist = Vector2()

    pos = Vector2()
    pos_last_tick = Vector2()
    movement = Vector2()

    @staticmethod
    def init():
        Mouse.pressed = np.array(False for _ in range(5))
        Mouse.just_pressed = Mouse.pressed.copy()
        Mouse.just_released = Mouse.pressed.copy()
        Mouse._pressed_last_tick = Mouse.pressed.copy()

    @staticmethod
    def tick():
        Mouse._pressed_last_tick = Mouse.pressed
        is_pressed = pygame.mouse.get_pressed(5)
        Mouse.pressed = np.array(is_pressed)

        Mouse.just_pressed = np.logical_and(
            np.logical_not(Mouse._pressed_last_tick), Mouse.pressed
        )
        Mouse.just_released = np.logical_and(
            Mouse._pressed_last_tick, np.logical_not(Mouse.pressed)
        )

        Mouse.pressed_left, Mouse.pressed_middle, Mouse.pressed_right = Mouse.pressed[
            :3
        ]
        (
            Mouse.just_pressed_left,
            Mouse.just_pressed_middle,
            Mouse.just_pressed_right,
        ) = Mouse.just_pressed[:3]
        (
            Mouse.just_released_left,
            Mouse.just_released_middle,
            Mouse.just_released_right,
        ) = Mouse.just_released[:3]

        Mouse.scroll_dist = Vector2()

        Mouse.pos_last_tick = Mouse.pos.copy()
        Mouse.pos[:] = pygame.mouse.get_pos()
        Mouse.movement = Mouse.pos - Mouse.pos_last_tick

    @staticmethod
    def events(event):
        if event.type == pygame.MOUSEWHEEL:
            Mouse.scroll_dist = event.x, event.y