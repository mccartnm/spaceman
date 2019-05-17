"""
The user interfacing
"""

import os
import math
import arcade

from ..core.settings import get_setting
from ..core.utils import Rect, Position
from ..core.damage import Damage
from ..core.player import Player

from .bar import Bar
from .button import Button
from .itembox import ItemBox
from .iabstract import TWidget


class _UI_ActiveItems(TWidget):
    """
    A bar of active items that reside on the bottom of our page
    """
    NUM_ITEMS = 10

    def __init__(self,
                 player: Player,
                 position: Position,
                 parent: TWidget = None):

        super().__init__(position, parent)
        self._player = player

        self._item_boxes = []
        for i in range(_UI_ActiveItems.NUM_ITEMS):
            box = ItemBox(self)
            box.local_geometry.move(Position(i * (40 * 1.5), 0))
            self._item_boxes.append(box)

class UserInterface(TWidget):
    """
    Host object for the users interface. This keeps track of a number of
    objects in the scene and the goings on of our ship and player inventory
    """

    def __init__(self, player: Player, parent: TWidget = None):
        super().__init__(Position(), parent)

        self._player = player

        resolution = Position(get_setting('resolution'))

        #
        # The beam representing our hull strength
        #
        self._health_bar = Bar(
            geometry=Rect(
                10, resolution.y - 30, resolution.x // 5, 20
            ),
            color=arcade.color.FOREST_GREEN,
            parent=self
        )

        #
        # The beam representing our current shields
        #
        self._shield_bar = Bar(
            geometry=Rect(
                10, resolution.y - 42, resolution.x // 5, 10
            ),
            color=arcade.color.DODGER_BLUE,
            parent=self
        )

        #
        # Energy bar to show how much power we're using/have left
        #
        self._energy_bar = Bar(
            geometry=Rect(
                10, resolution.y - 54, resolution.x // 5, 10
            ),
            color=arcade.color.GOLD,
            parent=self
        )

        #
        # Beam of objects and items the user is currently
        # working with. Attempt to center it on the screen
        #
        self._active_items = _UI_ActiveItems(
            self._player,
            Position(),
            self
        )

        size = self._active_items.size()
        self._active_items.set_position(Position(
            int((resolution.x - size.w) / 2),  10
        ))

        #
        # Listen for changes to the environment
        #
        self._listeners()

    def _listeners(self):

        # Start listening for damage events
        self._player.ship_took_damage.listen_post(
            self._calculate_ship_damage
        )

    @property
    def player(self):
        return self._player

    @property
    def ship(self):
        return self._player.ship

    # -- TSlots (although it's not really a thing)

    def _calculate_ship_damage(self, damage: Damage):
        """
        Based on the state of our ship, adjust the health
        and shield as needed

        Because we have to do a redraw anyways, we just set them
        both at once.
        """

        self._health_bar.set_percent(
            self.ship.hull / self.ship.hull_max
        )

        self._shield_bar.set_percent(
            self.ship.shield / self.ship.shield_max
        )
