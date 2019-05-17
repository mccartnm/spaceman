"""
Item storage tools
"""

import arcade

class _InventoryBase(object):

    def __init__(self):
        pass


class PlayerInventory(_InventoryBase):

    def __init__(self):
        super().__init__()