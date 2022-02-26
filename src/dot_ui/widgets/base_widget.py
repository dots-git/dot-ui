from re import S
from ..libraries import *
from .widget_behaviour import Behaviour

class Widget(object):
    renderer: type = None

    @staticmethod
    def set_renderer(renderer: type):
        Widget.renderer = renderer

    def __init__(self, x, y, width, height):
        self.pos = AnimVec([x, y])
        self.size = AnimVec([width, height])
        self.surface = Surface((width, height), pygame.SRCALPHA)
        
        self.behaviours: 'list[Behaviour]' = []

    def add_behaviour(self, trigger, function):
        self.behaviours.append(Behaviour(trigger, function))

    def _tick(self, delta):
        for behaviour in self.behaviours:
            if behaviour.trigger == 'tick':
                behaviour.function(self, delta)

        if self.size.target[0] < 0:
            self.size[0] = 0
        if self.size.target[1] < 0:
            self.size[1] = 0

        self.pos.tick(delta)
        self.size.tick(delta)

        if self.size[0] < 0:
            self.size._values[0] = 0
        if self.size[1] < 0:
            self.size._values[1] = 0

        if self.surface.get_size() != (round(self.size.x), round(self.size.y)):
            new_surface = pygame.Surface((round(self.size.x), round(self.size.y)), pygame.SRCALPHA)
            new_surface.blit(self.surface, (0, 0))
            self.surface = new_surface

    def _events(self, event):
        pass

    