import pygame
import numpy as np
from ..utils.vectors import Vector2


class Mouse:
    pressed = np.array([])
    pressed_left = False
    pressed_scroll = False
    pressed_right = False

    just_pressed = pressed.copy()
    just_pressed_left = False
    just_pressed_scroll = False
    just_pressed_right = False

    just_released = pressed.copy()
    just_released_left = False
    just_released_scroll = False
    just_released_right = False

    _pressed_last_tick = pressed.copy()
    _pressed_left_last_tick = False
    _pressed_scroll_last_tick = False
    _pressed_right_last_tick = False

    pos = Vector2()

    @staticmethod
    def init():
        Mouse.pressed = np.array(False for _ in range(5))
        Mouse.just_pressed = Mouse.pressed.copy()
        Mouse.just_released = Mouse.pressed.copy()
        Mouse._pressed_last_tick = Mouse.pressed.copy()

    @staticmethod
    def tick():
        Mouse._pressed_last_tick = Mouse.pressed
        is_pressed = pygame.mouse.get_pressed()
        Mouse.pressed = np.array(is_pressed)

        Mouse.just_pressed = np.logical_and(
            np.logical_not(Mouse._pressed_last_tick), Mouse.pressed
        )
        Mouse.just_released = np.logical_and(
            Mouse._pressed_last_tick, np.logical_not(Mouse.pressed)
        )

        Mouse.pressed_left, Mouse.pressed_scroll, Mouse.pressed_right = Mouse.pressed[
            :3
        ]
        (
            Mouse.just_pressed_left,
            Mouse.just_pressed_scroll,
            Mouse.just_pressed_right,
        ) = Mouse.just_pressed[:3]
        (
            Mouse.just_released_left,
            Mouse.just_released_scroll,
            Mouse.just_released_right,
        ) = Mouse.just_released[:3]

        Mouse.pos[:] = pygame.mouse.get_pos()
