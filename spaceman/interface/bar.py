"""
Progress bars, health bars, etc
"""

import arcade

from ..core.utils import Rect, Position

from .iabstract import _AbstractInterfaceObject


class Bar(_AbstractInterfaceObject):
    """
    Drawable bar
    """
    def __init__(self,
                 geometry: Rect = Rect(),
                 color = arcade.color.BLUE,
                 parent = None):

        super().__init__(geometry, parent)
        self._color = color

        # How much of our bar do we fill
        self._percent = 1.0

    @property
    def percent(self):
        return self._percent

    def set_percent(self, percent: float):
        self._percent = percent
        self.set_dirty(True)

    def shapes(self, draw_event):
        """
        Paint a basic beam
        """
        shapes = [self.background_shape()]

        rect = self.geometry.to_arcade_rect()
        shapes.append(arcade.create_rectangle(
            rect.x,
            rect.y,
            rect.w * self._percent,
            rect.h,
            self._color
        ))

        return shapes
