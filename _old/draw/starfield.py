"""
Simple starfield that understands paralax
"""

import os
import arcade
import random

from ..core.abstract import _AbstractDrawObject, DrawEvent
from ..core.utils import Depths, Position

class Starfield(_AbstractDrawObject):

    STAR_COUNT = 200.0

    def __init__(self, window, density: float = 1.0):
        super().__init__()

        self.set_z_depth(Depths.STAR_FIELD)

        self._window = window
        self._denisty = density

        self._small_stars = arcade.SpriteList()
        self._bigger_stars = arcade.SpriteList()
        self._build_star_layout()

    def set_density(self, density: float):
        """
        How populated is this starfield?
        """
        self._denisty = density

    def reset(self):
        """
        Create a new starfield
        """
        self._build_star_layout()

    def draw_method(self):
        """
        We paint things manually even though they are sprites
        """
        return _AbstractDrawObject.PAINT_BASED

    def paint(self, draw_event: DrawEvent):
        """
        We paint our starts manually given our points
        """
        self._small_stars.draw()
        self._bigger_stars.draw()

    def _build_star_layout(self):
        """
        Build a collection of stars
        """
        total_stars = int(self.STAR_COUNT * self._denisty)
        upper_third = total_stars // 3
        screen = Position(*self._window.get_size())

        # Go get our basic star texture. (3x3 gray tile ferda!)
        img = os.path.join(
            self._window.data_path, "objects", "space", "star.png"
        )
        for i in range(total_stars):

            if i < upper_third:
                l = self._bigger_stars
                scale = 1.4 * float(random.randrange(2))
            else:
                l = self._small_stars
                scale = 0.5 * float(random.randrange(2))

            s = arcade.Sprite(img, scale=scale)
            s.center_x = random.randrange(screen.x)
            s.center_y = random.randrange(screen.y)
            l.append(s)
