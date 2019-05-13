"""
The engines of a ship
"""

import os
import arcade

from .utils import _must_contain

class Engine(object):
    """
    An engine
    """
    WIDE = 'w' #< Takes two pixels for center
    THIN = 't' #< Takes one pixel for center

    def __init__(self, info):
        pass

    @classmethod
    def verify_ship_engine(cls, info, errors):
        """
        Verify that this engine information is enough to
        draw the dhip properly
        """
        if not isinstance(info, dict):
            errors.append("Engine should be a dictionary!")
            return

        map(lambda x: _must_contain(info, errors, *x), [
            ('location', list),
            ('size', str),
            ('default', str),
        ])

        if errors:
            return

        if info['size'] not in (cls.WIDE, cls.THIN):
            errors.append(
                f"Engine size must be one of: '{cls.WIDE}', '{cls.THIN}'"
            )

        location = info['location']
        if len(location) != 2:
            errors.append("'location' requires [x, y] coordinates")
        elif any((isinstance(x, int) == False for x in location)):
            errors.append("'location' components should be integers")

