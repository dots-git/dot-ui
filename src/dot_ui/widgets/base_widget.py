from ..libraries import *
from ..input.input_manager import *
from typing import Callable


class Behaviour:
    def __init__(self, name: str, tick_function: Callable):
        self.name = name
        self.tick_function = tick_function


class Widget(object):
    renderer: type = None

    @staticmethod
    def set_renderer(renderer: type):
        Widget.renderer = renderer

    def __init__(self, x=0, y=0, width=100, height=100, has_shadow=False, **kwargs):
        self.transform = AnimVec([x, y, width, height, 0])

        self.scale_around_center(self.size[:] * 0.5)
        self.transform.jump()
        self.scale_around_center(self.size[:] * 2)
        self.opacity = 1

        self.surface = Surface((width, height), pygame.SRCALPHA)

        self.behaviours: "list[Behaviour]" = []

        self.background_color: Color = None

        self._remove = False

        self.has_shadow = has_shadow

        self.parent: Widget = None

        for key in kwargs.keys():
            behaviour_keys = [
                "b_",
                "behav_",
                "behaviour_",
                "script_",
                "B_",
                "Behav_",
                "Behaviour_",
                "Script_"
            ]

            for behaviour_key in behaviour_keys:
                if key.startswith(behaviour_key):
                    item = kwargs[key]

                    tick_function = item
                    init_function = None

                    if isinstance(item, Iterable):
                        if len(item) > 0:
                            tick_function = item[0].tick
                        if len(item) > 1:
                            init_function = item[1].tick

                    self.add_behaviour(key[len(behaviour_key):], tick_function, init_function)

    def change_parent(self, new_parent):
        if self.parent is not None:
            self.parent.remove_widget(self)
        self.parent = new_parent

    def add_behaviour(self, name, tick_function=None, init_function=None):
        self.behaviours.append(Behaviour(name, tick_function))
        if init_function is not None:
            init_function(self)

    def close(self):
        self._remove = True
        self.opacity = 0
        self.scale_around_center(self.size[:] * 0.5)

    def scale_around_center(self, width, height=None):
        if height is None:
            array = iterable_to_array(width)
            width = array[0]
            height = array[1]
        self.transform._target[:2] += self.transform._target[2:4] / 2
        self.transform._target[2:4] = width, height
        self.transform._target[:2] -= self.transform._target[2:4] / 2

    def _init(self):
        self.init()

    def _tick(self, delta):

        if self._remove and self.transform.distance_to_target() < 1:
            self.parent.remove_widget(self)

        if not self._remove:
            for behaviour in self.behaviours:
                if behaviour.tick_function is not None:
                    behaviour.tick_function(self, delta)
        self.tick(delta)

        self.transform.tick(delta)

        if self._remove:
            self.surface = pygame.transform.scale(self.surface, self.size[:])
        elif self.surface.get_size() != (
            round(self.transform[2]),
            round(self.transform[3]),
        ):
            new_surface = pygame.Surface(
                (abs(round(self.transform[2])), abs(round(self.transform[3]))),
                pygame.SRCALPHA,
            )
            new_surface.blit(self.surface, (0, 0))
            self.surface = new_surface

    def _events(self, event):
        pass

    def init(self):
        pass

    def tick(self, delta):
        pass

    @property
    def pos(self) -> IVecAnim:
        return IVecAnim(self.transform, 0, 2)

    @pos.setter
    def pos(self, value):
        if isinstance(value, IVecAnim):
            value = value._anim_vec.target[value._start_index : value._end_index]
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
