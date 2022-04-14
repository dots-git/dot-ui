from math import exp
from dot_ui.utils.vectors import Vector2
from simple_pg import *
import dot_ui.utils.draw as draw_utils
from dot_ui.utils.animations import AnimVec
from dot_ui.utils.color_constants import RED, WHITE

class WaveRipple:
    all_ripples: "list[WaveRipple]" = []

    def __init__(self):
        self.x = None
        self.y = None

        self.inner_size = AnimVec()
        self.inner_size.acceleration = 300
        self.inner_size.drag = 3

        self.outer_size = AnimVec()
        self.outer_size.acceleration = 700
        self.outer_size.drag = 4

        self.inner_size[0] = 26
        self.outer_size[0] = 30

        self.released = False

        self.pos_last_tick = Vector2(0, 0)
        self.velocity = Vector2(0, 0)

        WaveRipple.all_ripples.append(self)
    
    def tick(self, delta):
        if self.x is None or self.y is None:
            x, y = pygame.mouse.get_pos()
        else:
            x, y = self.x, self.y

        self.inner_size.tick(delta)
        self.outer_size.tick(delta)
        
        if self.inner_size[0] > self.outer_size[0]:
            WaveRipple.all_ripples.remove(self)
        
        if self.released:
            vel_x, vel_y = (self.velocity * delta).asarray()
            self.x += vel_x
            self.y += vel_y

            self.velocity *= exp(-delta * 19)
        else:  
            pos_rn = Vector2(x, y)
            self.velocity = (pos_rn - self.pos_last_tick) / delta
            self.pos_last_tick = pos_rn

    def draw(self):
        if self.x is None or self.y is None:
            x, y = pygame.mouse.get_pos()
        else:
            x, y = self.x, self.y
        circle(
            x,
            y,
            self.outer_size.x,
            color=RED,
        )
        circle(
            x,
            y,
            self.inner_size.x,
            color=WHITE,
        )
    
    def release(self, pos):
        self.released = True
        self.x, self.y = pos
        self.inner_size[0] = 42
        self.outer_size[0] = 40

def events(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        WaveRipple()
    if event.type == pygame.MOUSEBUTTONUP:
        for ripple in WaveRipple.all_ripples:
            ripple.release(event.pos)

def draw():
    for ripple in WaveRipple.all_ripples:
        ripple.draw()

def tick(delta):
    for ripple in WaveRipple.all_ripples:
        ripple.tick(delta)

go(init, tick_func=tick, events_fuc=events)