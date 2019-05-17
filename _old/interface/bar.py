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
    MIDDLE_OUT = 'mi'
    RIGHT_TO_LEFT = 'rtl'

    def __init__(self,
                 geometry: Rect = Rect(),
                 color = arcade.color.BLUE,
                 parent = None):

        super().__init__(geometry, parent)
        self._color = color

        self._mode = Bar.MIDDLE_OUT

        # How much of our bar do we fill
        self._percent = 1.0

    @property
    def percent(self):
        return self._percent

    @property
    def mode(self):
        return self._mode

    def set_mode(self, mode: str):
        if not mode in (Bar.MIDDLE_OUT, Bar.RIGHT_TO_LEFT):
            return
        self._mode = mode

    def set_percent(self, percent: float):
        self._percent = percent
        self.set_dirty(True)

    def shapes(self, draw_event):
        """
        Paint a basic beam
        """
        shapes = [self.background_shape()]

        rect = self.geometry

        if self._mode == Bar.RIGHT_TO_LEFT:
            rect = Rect(
                rect.x, rect.y, rect.w * self._percent, rect.h
            ).to_arcade_rect()
        elif self._mode == Bar.MIDDLE_OUT:
            rect = rect.to_arcade_rect()
            rect = Rect(
                rect.x, rect.y, rect.w * self._percent, rect.h
            )

        shapes.append(arcade.create_rectangle(
            *(rect),
            self._color
        ))

        return shapes
