"""
Damage controls
"""

import arcade

class Damage(object):
    """
    Object that contains a select damage amount and type
    """
    PIERCE     = "pierce"
    EXPLOSILVE = "explosive"
    ENERGY     = "energy"
    NULL       = "null"

    DAMAGE_TYPES = (PIERCE, EXPLOSILVE, ENERGY, NULL)

    def __init__(self, type_: str, amount: (int, float) = 0):
        self._type = type_
        self._amount = amount

    def __repr__(self):
        return f"<(Damage, {self._type}: {self._amount})>"

    @property
    def type_(self):
        return self._type
    
    @property
    def amount(self):
        return self._amount
