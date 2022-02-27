from ..libraries import *
from .widget_behaviour import Behaviour
from ..input.input_manager import *


class Widget(object):
    renderer: type = None

    @staticmethod
    def set_renderer(renderer: type):
        Widget.renderer = renderer

    def __init__(self, x, y, width, height):
        self.transform = AnimVec([x, y, width, height, 0])

        self.scale_around_center(self.size[:] * 0.5)
        self.transform.jump()
        self.scale_around_center(self.size[:] * 2)
        self.opacity = 1

        self.surface = Surface((width, height), pygame.SRCALPHA)

        self.behaviours: "list[Behaviour]" = []

        self.has_shadow = True

        self.background_color = None

        self._remove = False
        self._is_garbage = False

    def add_behaviour(self, trigger, function):
        self.behaviours.append(Behaviour(trigger, function))

    def remove(self):
        self._remove = True
        self.opacity = 0
        self.scale_around_center(self.size[:] * .5)

    def scale_around_center(self, width, height = None):
        if height is None:
            array = iterable_to_array(width)
            width = array[0]
            height = array[1]
        self.transform._target[:2] += self.transform._target[2:4] / 2
        self.transform._target[2:4] = width, height
        self.transform._target[:2] -= self.transform._target[2:4] / 2


    def _tick(self, delta):

        if self._remove and self.transform.distance_to_target() < 1:
            self._is_garbage = True

        if not self._remove:
            for behaviour in self.behaviours:
                if behaviour.trigger == "tick":
                    behaviour.function(self, delta)

        self.transform.tick(delta)

        if self.surface.get_size() != (
            round(self.transform[2]),
            round(self.transform[3]),
        ):
            new_surface = pygame.Surface(
                (abs(round(self.transform[2])), abs(round(self.transform[3]))), pygame.SRCALPHA
            )
            new_surface.blit(self.surface, (0, 0))
            self.surface = new_surface

    def _events(self, event):
        pass

    @property
    def pos(self) -> IVecAnim:
        return IVecAnim(self.transform, 0, 2)

    @pos.setter
    def pos(self, value):
        self.transform[:2] = value[:]

    @property
    def size(self) -> IVecAnim:
        return IVecAnim(self.transform, 2, 4)

    @size.setter
    def size(self, value):
        self.transform[2:4] = value[:]

    @property
    def opacity(self) -> float:
        return self.transform[4]
    
    @opacity.setter
    def opacity(self, value):
        self.transform[4] = value

size