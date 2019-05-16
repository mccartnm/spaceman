"""
The user interfacing
"""

import os
import math
import arcade

from .bar import Bar
from .iabstract import TWidget

from ..core.settings import get_setting
from ..core.utils import Rect, Position

class UserInterface(TWidget):
    """
    Host object for the users interface. This keeps track of a number of
    objects in the scene
    """

    def __init__(self, player):
        super().__init__()

        self._player = player

        resolution = Position(get_setting('resolution'))

        self._health_bar = Bar(
            geometry=Rect(
                10, resolution.y - 30, resolution.x // 5, 20
            ),
            color=arcade.color.FOREST_GREEN,
            parent=self
        )

        self._shield_bar = Bar(
            geometry=Rect(
                10, resolution.y - 40, resolution.x // 5, 10
            ),            
            color=arcade.color.DODGER_BLUE,
            parent=self
        )

    @property
    def player(self):
        return self._player
