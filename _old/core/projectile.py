"""
Tools for the firing of things!
"""

import os
import math
import arcade

from . import settings
from .abstract import _AbstractDrawObject
from .utils import Position

class Bullet(_AbstractDrawObject):
    """
    Shoot to kill!
    """

    # Location to find bullet images
    _data_directory = ""

    def __init__(self,
                 name: str,
                 damage: (int, float),
                 origin: Position,
                 range_: (int, float),
                 owner: _AbstractDrawObject):
        """
        Construct a bullet!
        """
        super().__init__()
        self._name = name
        self._damage = damage
        self._origin = origin
        self._range = range_
        self._owner = owner

        self.set_z_depth(self._owner.z_depth - 1)
        self._speed = 13
        self._traveled = 0

    @classmethod
    def set_data_directory(cls, data_directory: str):
        """
        Set the classwide data directory
        """
        cls._data_directory = data_directory

    def draw_method(self):
        """
        Bullets are a simple sprite
        """
        return _AbstractDrawObject.SPRITE_BASED

    def load_sprite(self):
        """
        Get the bullet sprite
        """
        s = self.load_basic(Bullet._data_directory, self._name)        
        s.set_position(self._origin)
        s.angle = self._owner.angle

        radians = math.radians(self._owner.angle)
        s.change_y = math.cos(radians) * self._speed
        s.change_x = -math.sin(radians) * self._speed
        return s

    def update(self, delta_time):
        """
        We have to move the bullet along based on the velocity
        :return: bool - False if this item is being staged for deletion
        """
        self._traveled += self._speed
        if self._traveled > self._range:
            # We've gone passed our range - time to die
            self.remove_from_scene()
            self.sprite().kill() # Just in case
            return False

        super().update(delta_time)
        return True
