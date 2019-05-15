"""
Class for handling hardpoints and weapons
"""

import os
import yaml
import arcade

from .utils import _must_contain, emap
from .abstract import _AbstractDrawObject, TSprite

class Hardpoint(_AbstractDrawObject):
    """
    A hardpoint is a single location that can host
    a weapon of some sort
    """

    # The various types of hardpoints we support
    BULLET  = 'bullet'
    LAZER   = 'lazer'
    BOMB    = 'bomb'
    MISSILE = 'missile'
    MINER   = 'miner'
    UTILITY = 'utility'
    HARDPONT_TYPES = (BULLET, LAZER, BOMB, MISSILE, MINER, UTILITY)

    # -- Known - loaded hardpoint descriptors
    _hardpoint_prototypes = {}

    def __init__(self, hardpoint_info, ship_hardpoint_info, ship):
        super().__init__()
        self._name      = hardpoint_info['name']
        self._ammo      = hardpoint_info['description']
        self._type      = hardpoint_info['type']
        self._location  = hardpoint_info['ammo']
        self._damage    = hardpoint_info['damage']
        self._command   = hardpoint_info['rate']
        self._ship_hi   = ship_hardpoint_info
        self._ship      = ship

        # For items that are "on/off" e.g. lazers, miner,
        # automatic bullets, etc
        self._on = False

    def __repr__(self):
        return f"<(Hardpoint, {self._name})>"

    @classmethod
    def new_hardpoint(cls, prototype: str, sinfo: dict, ship):
        return cls(cls._hardpoint_prototypes[prototype], sinfo, ship)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def ammo(self):
        return self._ammo

    @property
    def location(self):
        return self._location

    @property
    def direction(self):
        return self._direction

    @property
    def locked(self):
        return self._locked

    @property
    def damage(self):
        return self._damage

    @property
    def command(self):
        return self._command

    def fire(self):
        """
        If possible - use this item.

        For projectiles, we check our ships ammo (unless the ammo type is None)

        For things like lazers/utlity items, they will consume energy when used
        unless they are passives.
        """
        if self._type == Hardpoint.BULLET:
            # A projectile with a b-line path
            pass


    @classmethod
    def add_info_file(cls, info_file: str, info_dir: str):
        """
        Load multiple hardpoint descriptors from a file
        """
        errors = []
        if not os.path.isfile(info_file):
            raise RuntimeError(
                f"Info for {info_file} does not exist!"
            )

        try:
            with open(info_file, 'r') as f:
                info = yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(str(e))

        if not isinstance(info, list):
            raise RuntimeError(
                f"Info for {info_file} must be a list[dict,]"
            )

        for hp_info in info:
            if not isinstance(hp_info, dict):
                raise RuntimeError(
                    f"Each descriptor for {info_file} must be a dict"
                )

            emap(lambda x: _must_contain(hp_info, errors, *x), [
                ('name', str),
                ('description', str),
                ('type', str),
                ('ammo', (str, type(None))),
                ('damage', (int, float)),
                ('rate', (int, float)),
            ])

            n = hp_info.get('name', info_file)
            if errors:
                print (f"ERROR ON: {n}:")
                print ("\n".join(errors))
                raise RuntimeError("Could not start game")

            if n in cls._hardpoint_prototypes:
                raise RuntimeError(f"Duplicate hardpoint name: {n}! Must be unique!")

            cls._hardpoint_prototypes[n] = hp_info

    @classmethod
    def verify_ship_hardpoint(cls, info: dict, errors: list):
        """
        Verify that this hardpoint information is enough to
        create a hardpoint properly
        :param info: dict of information
        :param errors: Accumulated errors
        :return: None
        """
        if not isinstance(info, dict):
            errors.append(f"Hardpoint should be a dictionary!")
            return

        emap(lambda x: _must_contain(info, errors, *x), [
            ('name', str),
            ('types', list),
            ('location', list),
            ('direction', (int, float)),
            ('locked', (int, float)),
            ('command', str),
            ('default', (str, type(None))),
        ])

        if errors:
            return

        if info['default'] not in cls._hardpoint_prototypes:
            errors.append(
                f'Unknown hardpoint prototype: {info["default"]}'
            )

        types = info['types']
        if any(((t not in cls.HARDPONT_TYPES) for t in types)):
            errors.append(
                f"{info['types']} Types must be one of: {cls.HARDPONT_TYPES}"
            )

        location = info['location']
        if len(location) != 2:
            errors.append("'location' requires [x, y] coordinates")
        elif any((isinstance(x, int) == False for x in location)):
            errors.append("'location' components should be integers")

    def draw_method(self):
        return _AbstractDrawObject.PAINT_BASED

    def paint(self, draw_event):
        """ For now do nothing """
        pass