import arcade

import time
import collections

from typing import TypeVar

def _clamp(low, val, high):
    return max(min(val, high), low)

def emap(predicate, iterable):
    """
    Pyhton 3 evaluates lazy. Which is cool. But we don't always want that

    We do this in a for loop to take advantage of the memory benefits rather
    than storing everyhting in a list.
    """
    for foo in map(predicate, iterable):
        pass

def _must_contain(info: dict, errors: list, *d):
    """
    For yaml validation, we use this function a _lot_
    :param info: The information dictionary that we're looking for
    :param errors: list[str] of errors that we'll fill when something
    goes wrong
    :param d: arguments of (key, type|tuple(type,)) for instance
    checking
    :return: None
    """
    key, is_type = d
    if key not in info:
        errors.append(f"Missing key: '{key}'")
    elif not isinstance(info[key], is_type):
        errors.append(f"'{key}' wrong type! Should be: {is_type}")

T = TypeVar('T', bound='Position')

class Position(object):
    """
    Basic (x, y) coordinates with helper functions
    """

    def __init__(self, x: (int, float, tuple, list) = [0, 0], y: (int, float, type(None)) = None):
        if y is None:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __eq__(self, other):
        """ Equatative math """
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        """ Subtractive math """
        return Position(self.x - other.x, self.y - other.y)

    def __add__(self, other: T) -> T:
        """ Additive math """
        return Position(self.x + other.x, self.y + other.y)

    def __mul__(self, other: (int, float, T)) -> T:
        """ Multiplication """
        if isinstance(other, Position):
            return Position(self.x * other.x, self.y * other.y)
        return Position(self.x * other, self.y * other)
        
    def __repr__(self):
        return f"<(Position ({self.x}, {self.y}))>"

    def drag_calculation(self, drag: T) -> T:
        """
        Basic drag math over a frame
        """
        def _d_neg(v, o):
            return max(v - o, 0.0)

        if self.x > 0:
            self.x = _d_neg(self.x, drag.x)
        if self.y > 0:
            self.y = _d_neg(self.y, drag.y)

        def _d_pos(v, o):
            return min(v + o, 0.0)

        if self.x < 0:
            self.x = _d_pos(self.x, drag.x)
        if self.y < 0:
            self.y = _d_pos(self.y, drag.y)

        return self

    def clamp(self, minimum: (int, float, T), maximum: (int, float, T)) -> T:
        """
        Basic clamping mathmatics
        :param minimum: Value to stay above for X and Y or a Position to clamp individually
        :param maximum: Value to stay below for X and Y or a Position to clamp individually
        :return: self
        """
        low_x = 0
        low_y = 0
        high_x = 0
        high_y = 0
        if isinstance(minimum, Position):
            low_x = minimum.x
            low_y = minimum.y
        else:
            low_x = low_y = minimum

        if isinstance(maximum, Position):
            high_x = maximum.x
            high_y = maximum.y
        else:
            high_x = high_y = maximum

        self.x = _clamp(low_x, self.x, high_x)
        self.y = _clamp(low_y, self.y, high_y)
        return self

class Depths(object):
    """
    Constant depths that we use throughout the game
    """
    STAR_FIELD = -100
    PLAYER = 0


class FPSCounter(object):
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)