"""
Simple starfield that understands paralax
"""

import arcade
import random

from ..core.abstract import _AbstractDrawObject, DrawEvent
from ..core.utils import Depths, Position

class Starfield(_AbstractDrawObject):

    STAR_COUNT = 100.0

    def __init__(self, window, density: float = 1.0):
        super().__init__()

        self.set_z_depth(Depths.STAR_FIELD)

        self._window = window
        self._denisty = density

        self._stars = []
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
        We paint things manually
        """
        return _AbstractDrawObject.PAINT_BASED

    def paint(self, draw_event: DrawEvent):
        """
        We paint our starts manually given our points
        """
        arcade.draw_points(self._stars[0], arcade.csscolor.AZURE, 4)
        arcade.draw_points(self._stars[1], arcade.csscolor.DIM_GREY, 4)

    def _build_star_layout(self):
        """
        Build a collection of stars
        """
        self._stars = [[], []]

        total_stars = int(self.STAR_COUNT * self._denisty)
        large_to_small = total_stars // 3
        screen = Position(*self._window.get_size())

        for i in range(total_stars):
            if i < large_to_small:
                idx = 0
            else:
                idx = 1

            self._stars[idx].append(
                [random.randrange(screen.x), random.randrange(screen.x)]
            )

        self._stars = (tuple(self._stars[0]), tuple(self._stars[1]))
