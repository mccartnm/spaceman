
import arcade

from . import inventory

class Player(object):
    """
    The player attributes!
    """

    def __init__(self):
        self._ship = None
        self._inventory = inventory.PlayerInventory()