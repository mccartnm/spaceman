"""
Class for handling hardpoints and weapons
"""

import os
import yaml
import arcade

from .utils import _must_contain

class Hardpoint(object):
    """
    A hardpoint is a single location that can host
    a weapon of some sort
    """

    # The various types of hardpoints we support
    BULLET = 'bullet'
    LAZER = 'lazer'
    BOMB = 'bomb'
    MISSILE = 'missile'
    MINER = 'miner'
    HARDPONT_TYPES = (BULLET, LAZER, BOMB, MISSILE, MINER)

    # -- Known - loaded hardpoint descriptors
    _hardpoint_prototypes = {}

    def __init__(self, info):
        self._name      = info['name']
        self._type      = info['type']
        self._ammo      = info['ammo']
        self._location  = info['location']
        self._direction = info['direction']
        self._locked    = info['locked']
        self._damage    = info['damage']
        self._command   = info['command']

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
                f"Info for {info_file} must be a list"
            )

        for hp_info in info:
            if not isinstance(hp_info, dict):
                raise RuntimeError(
                    f"Each info for {info_file} must be a list"
                )

            map(lambda x: _must_contain(hp_info, errors, *x), [
                ('name', str),
                ('description', str),
                ('type', str),
                ('ammo', (str, type(None))),
                ('damage', (int, float)),
                ('rate', (int, float)),
            ])

            n = hp_info.get('name', info_file)
            if errors:
                print ("ERROR ON: {n}:")
                print ("\n".join(errors))
                raise RuntimeError("Could not start game")

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

        map(lambda x: _must_contain(info, errors, *x), [
            ('name', str),
            ('types', list),
            ('location', str),
            ('direction', (int, float)),
            ('locked', (int, float)),
            ('command', str),
            ('default', str),
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

