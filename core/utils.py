
import arcade

def _must_contain(info, errors, *d):
    key, is_type = d
    if key not in info:
        errors.append(f"Missing key: '{key}'")
    elif not isinstance(info[key], is_type):
        errors.append(f"'{key}' wrong type! Should be: {is_type}")

class Position(object):
    """ Basic (x, y) coordinates with helper functions"""
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return Position(self.x - x, self.y - y)

    def __rsub__(self, val):
        if isinstance(val, Position):
            self.x -= val.x
            self.y -= val.y
        else:
            self.x - val
            self.y - val

    def __add__(self, other):
        return Position(self.x + x, self.y + y)

    def __radd__(self, val):
        if isinstance(val, Position):
            self.x += val.x
            self.y += val.y
        else:
            self.x + val
            self.y + val
