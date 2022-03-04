from copy import copy
from .animations import AnimVec
from math import sqrt, atan2
from .general import *


class Vector2:
    def __init__(self, x=0, y=None):
        self.x = x
        self.y = y

        if y is None:
            if isinstance(x, (int, float)):
                self.y = x
            elif isinstance(x, Iterable):
                array = iterable_to_array(x)
                self.y = array[1]
                self.x = array[0]

    def length_squared(self):
        return self.x * self.x + self.y * self.y

    def length(self):
        return sqrt(self.length_squared())

    def distance_squared(self, other: "Vector2"):
        return (self - other).length_squared()

    def distance(self, other: "Vector2"):
        return (self - other).length()

    def angle(self, other: "Vector2"):
        return atan2(self.y - other.y, self.x - other.x)

    def point_angle(self, other: "Vector2", reference: "Vector2" = (0, 1)):
        if reference is None:
            reference = Vector2(0, 1)
        return (other - self).angle(reference)

    def dot(self, other: "Vector2"):
        return self.x * other.x + self.y * other.y

    def normalized(self):
        return self / self.length()

    def asarray(self):
        return np.asarray([self.x, self.y])

    def copy(self):
        return Vector2(self.x, self.y)

    def in_rect(self, x, y=None, width=None, height=None):
        if y is None or width is None or height is None:
            pos = x[:2]
            size = None
            if width is None:
                size = x[2:4]
            elif height is None:
                size = width[:2]
            x, y = pos
            if size is not None: width, height = size
            
        return x < self.x < x + width and y < self.y < y + height
    
    def round(self):
        return Vector2(round(self.x), round(self.y))
    
    def floor(self):
        return Vector2(floor(self.x), floor(self.y))
    
    def roof(self):
        return Vector2(roof(self.x),  roof(self.y) )

    def __getitem__(self, index):
        return self.asarray()[index]

    def __setitem__(self, index, value):
        array = self.asarray()
        array[index] = value
        self.x, self.y = array

    def __sub__(self, other: "Vector2"):
        return Vector2(self.x - other.x, self.y - other.y)

    def __add__(self, other: "Vector2"):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: "Vector2 | float | int"):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: "Vector2 | float | int"):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)
    
    def __eq__(self, other: "Vector2"):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return type(self).__name__ + "(" + str(self.x) + ", " + str(self.y) + ")"


class IVecAnim(Vector2):
    def __init__(self, anim_vec: AnimVec, start_index, end_index):
        self._anim_vec = anim_vec
        self._start_index = start_index
        self._end_index = end_index

    @property
    def x(self):
        return self._anim_vec[self._start_index]

    @x.setter
    def x(self, value):
        self._anim_vec[self._start_index] = value

    @property
    def y(self):
        return self._anim_vec[self._start_index + 1]

    @y.setter
    def y(self, value):
        self._anim_vec[self._start_index + 1] = value

    def __getitem__(self, index):
        return self._anim_vec[self._start_index : self._end_index][index]

    def __setitem__(self, index, value):
        self._anim_vec[self._start_index : self._end_index][index] = value

    def jump(self):
        for i in range(self._start_index, self._end_index):
            self._anim_vec.jump(i)

    def __iadd__(self, other: Vector2):
        self._anim_vec._target[self._start_index : self._end_index] += other.asarray()
        return self

    def __isub__(self, other: Vector2):
        self._anim_vec._target[self._start_index : self._end_index] -= other.asarray()
        return self

    def __imul__(self, other: Vector2):
        self._anim_vec._target[self._start_index : self._end_index] *= other.asarray()
        return self

    def __idiv__(self, other: Vector2):
        self._anim_vec._target[self._start_index : self._end_index] /= other.asarray()
        return self
