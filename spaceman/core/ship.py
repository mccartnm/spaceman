"""
Base classes for the ships (player or NPC)
"""

import os
import yaml
import arcade

from .abstract import _AbstractDrawObject, TSprite
from .hardpoint import Hardpoint
from .engine import Engine
from .utils import _must_contain, Position
from . import settings

class ShipHardpoint(object):
    """
    A ship hardpoint can hold onto a Hardpoint object to interact
    with the world in some way (weapons, research, mining, etc)
    """

    def __init__(self, info):
        self._name      = info['name']
        self._types     = info['types']
        self._location  = info['location']
        self._direction = info['direction']
        self._locked    = info['locked']
        self._command   = info['command']
        self._default   = info['default']

        # The currently attached hardpoint
        self._hardpoint = None

class ShipEngine(object):
    """
    A ship engine 
    """
    def __init__(self, info):
        self._location = info['location']
        self._size     = info['size']
        self._default  = info['default']

class Ship(_AbstractDrawObject):
    """
    A component that can float/fly in space, has health, can be destroyed,
    and other fin stuff!
    """
    _ship_prototypes = {}

    def __init__(self, ship_info):
        """
        Building a ship takes a good chunk of information
        """
        super().__init__()

        # All the defaults
        self._display_name = ship_info['display_name']
        self._class        = ship_info['class']
        self._description  = ship_info['description']
        self._mobile       = ship_info['mobile']
        self._hull         = ship_info['hull']
        self._shield       = ship_info['shield']
        self._fuel         = ship_info['fuel']

        self._hardpoints   = [
            ShipHardpoint(x) for x in ship_info.get('hardpoints', [])
        ]

        self._engines      = [
            ShipEngine(x) for x in ship_info.get('engines', [])
        ]

        self._data_location = ship_info['data_directory']

    @property
    def display_name(self):
        return self._display_name

    @property
    def class_(self):
        return self._class

    @property
    def description(self):
        return self._description
    
    @property
    def hull(self):
        return self._hull

    @property
    def shield(self):
        return self._shield

    @property
    def hardpoints(self):
        return self._hardpoints

    def draw_method(self):
        """ This is a sprite based object """
        return _AbstractDrawObject.SPRITE_BASED

    def load_sprite(self):
        """
        We load the ship for various reasons
        """
        return self.default_sprite(self._data_location)

    @classmethod
    def new_ship(cls, name: str, position: Position = Position(10, 10)):
        """
        Build and return a ship object to the game instance 
        """
        if name not in cls._ship_prototypes:
            raise RuntimeError(f"Unknown ship prototype: {name}")

        ship = Ship(cls._ship_prototypes[name])
        ship.set_position(position)
        return ship

    @classmethod
    def add_prototype(cls, name: str, info_file: str):
        """
        Verify all the information from a .si file
        :param name: The name of the ship
        :param info_file: The .si file that should conatin the ship info
        :return: tuple(list[str], dict|None) (errors, information)
        """
        errors = []
        if not os.path.isfile(info_file):
            raise RuntimeError(
                f"Could not start game! {name} info file needed"
            )

        try:
            with open(info_file, 'r') as f:
                info = yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(str(e))

        if not isinstance(info, dict):
            # We can't load anything else
            raise RuntimeError(f"Info for {name} must be a dictionary")

        map(lambda x: _must_contain(info, errors, *x), [
            ('display_name', str),
            ('class', str),
            ('description', str),
            ('mobile', bool),
            ('hull', int),
            ('shield', int),
            ('fuel', int),
        ])

        # If there are hardpoints...
        if 'hardpoints' in info:
            if not isinstance(info['hardpoints'], list):
                errors.append("Hardpoints must be a list of dictionaries")
            else:
                for hp_info in info['hardpoints']:
                    hp_errors = []
                    Hardpoint.verify_ship_hardpoint(hp_info, hp_errors)
                    if hp_errors:
                        errors.append("Hardpoint failure:")
                        errors.extend(hp_errors)

        # If there are engines...
        if 'engines' in info:
            if not isinstance(info['engines'], list):
                errors.append("Engines must be a list of dictionaries")
            else:
                for engine_info in info['engines']:
                    engine_errors = []
                    Engine.verify_ship_engine(engine_info, engine_errors)
                    if engine_errors:
                        errors.append("Engine failure:")
                        errors.extend(engine_errors)

        # At a minimum there must be one sprite of "life/static.png"
        path = os.path.join(os.path.dirname(info_file), 'life/static.png')
        if not os.path.isfile(path):
            errors.append("life/static.png is required for all ships")

        if errors:
            print ("\n".join(errors))
            raise RuntimeError(
                f"Could not start game! Loading error on: '{name}'"
            )

        info['data_directory'] = os.path.dirname(info_file)
        cls._ship_prototypes[info['display_name']] = info


    def _load_sprites(self, data_location):
        """
        Find the various sprites that we're want to load.
        Because we do all sprite requests dynamically
        :param data_location: The root location of the files that
        we want to use
        :return: None
        """


        # "Life" setup
        # for 
