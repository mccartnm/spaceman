
import arcade

from . import inventory
from .ship import Ship

class Player(object):
    """
    The player attributes!
    """

    def __init__(self):
        self._ship = None
        self._inventory = inventory.PlayerInventory()

    @property
    def ship(self):
        return self._ship

    def set_ship(self, ship: Ship):
        """
        Set the players active ship
        """
        self._ship = ship
