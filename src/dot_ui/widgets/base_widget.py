from tkinter import W
from ..libraries import *

class Widget(object):
    renderer: type = None

    @staticmethod
    def set_renderer(renderer: type):
        Widget.renderer = renderer

    def __init__(self, x, y, width, height):
        self._super_init(x, y, width, height)

    def _super_init(self, x, y, width, height):
        self.pos = AnimVec([x, y])
        self.size = AnimVec([width, height])
        self.surface = Surface((width, height), pygame.SRCALPHA)

    def set_size(self):
        pass

    def _events(self, event):
        pass