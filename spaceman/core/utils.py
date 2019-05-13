
import arcade

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

class Position(object):
    """
    Basic (x, y) coordinates with helper functions
    """

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """ Equatative math """
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        """ Subtractive math """
        return Position(self.x - x, self.y - y)

    def __rsub__(self, val):
        """ Reference sub, supports both unary and Position values """
        if isinstance(val, Position):
            self.x -= val.x
            self.y -= val.y
        else:
            self.x - val
            self.y - val

    def __add__(self, other):
        """ Additive math """
        return Position(self.x + x, self.y + y)

    def __radd__(self, val):
        """ Reference add, supports both unary and Position values """
        if isinstance(val, Position):
            self.x += val.x
            self.y += val.y
        else:
            self.x + val
            self.y + val


class Depths(object):
    """
    Constant depths that we use throughout the game
    """
    STAR_FIELD = -100
    PLAYER = 0
