"""
Tools for the firing of things!
"""

import os
import arcade

from .abstract import _AbstractDrawObject

class Bullet(_AbstractDrawObject):
    """
    Shoot to kill!
    """

    # Location to find bullets
    _bullet_data_directory = ""

    def __init__(self, name, damage, ship):
        """
        Construct a bullet!
        """
        super().__init__()
        self._name = name
        self._damage = damage
        self._ship = ship

    @classmethod
    def set_data_directory(cls, data_directory: str):
        """
        Set the classwide data directory
        """
        cls._bullet_data_directory = data_directory

    def draw_method(self):
        return _AbstractDrawObject.PAINT_BASED

    def load_sprite(self):
        """
        Get the bullet sprite
        """
        pass
