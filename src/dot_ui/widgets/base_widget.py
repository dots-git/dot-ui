from ..libraries import *
from .widget_behaviour import Behaviour
from ..input.input_manager import *


class Widget(object):
    renderer: type = None

    @staticmethod
    def set_renderer(renderer: type):
        Widget.renderer = renderer

    def __init__(self, x, y, width, height):
        self.transform = AnimVec([x, y, width, height])
        self.surface = Surface((width, height), pygame.SRCALPHA)

        self.behaviours: "list[Behaviour]" = []

        self.has_shadow = True

    def add_behaviour(self, trigger, function):
        self.behaviours.append(Behaviour(trigger, function))

    def _tick(self, delta):

        pass

        for behaviour in self.behaviours:
            if behaviour.trigger == "tick":
                behaviour.function(self, delta)

        if self.transform.target[2] < 0:
            self.transform[2] = 0
        if self.transform.target[3] < 0:
            self.transform[3] = 0

        self.transform.tick(delta)

        if self.transform[2] < 0:
            self.transform._values[2] = 0
        if self.transform[3] < 0:
            self.transform._values[3] = 0

        if self.surface.get_size() != (
            round(self.transform[2]),
            round(self.transform[3]),
        ):
            new_surface = pygame.Surface(
                (round(self.transform[2]), round(self.transform[3])), pygame.SRCALPHA
            )
            new_surface.blit(self.surface, (0, 0))
            self.surface = new_surface

    def _events(self, event):
        pass

    @property
    def pos(self):
        return IVecAnim(self.transform, 0, 2)

    @pos.setter
    def pos(self, position):
        self.transform[:2] = position[:]

    @property
    def size(self):
        return IVecAnim(self.transform, 2, 4)

    @size.setter
    def size(self, size):
        self.transform[2:] = size[:]
