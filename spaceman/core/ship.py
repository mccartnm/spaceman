"""
Base classes for the ships (player or NPC)
"""

import os
import math
import yaml
import arcade
import functools

from .abstract import _AbstractDrawObject, TSprite
from .hardpoint import Hardpoint
from .engine import Engine
from .utils import _must_contain, Position, emap
from . import settings

class ShipHardpoint(object):
    """
    Proxy object for a Hardpoint that it set on the ship

    A ship hardpoint can hold onto a Hardpoint object to interact
    with the world in some way (weapons, research, mining, etc)
    """

    def __init__(self, info, ship):
        # self._name      = info['name']
        # self._types     = info['types']
        # self._location  = info['location']
        # self._direction = info['direction']
        # self._locked    = info['locked']
        # self._command   = info['command']
        # self._default   = info['default']
        self._info = info
        self._ship = ship

        # The currently attached hardpoint (Set to default)
        self._hardpoint = None
        if self.default:
            self._hardpoint = Hardpoint.new_hardpoint(self.default, info, ship)

    def __getattr__(self, attr):
        """
        We reroute requests we don't have the answer for to our engine
        """
        if attr in self._info:
            return self._info[attr]

        if self._hardpoint:
            return getattr(self._hardpoint, attr)
        raise RuntimeError(f"Unknown engine property: {attr}")

    @property
    def hardpoint(self):
        return self._hardpoint


class ShipEngine(object):
    """
    Proxy object for an Engine that it set on the ship
    """
    def __init__(self, info, ship):
        # self._location = info['location']
        # self._size     = info['size']
        # self._default  = info['default']
        self._info = info
        self._ship = ship

        # The currently attached engine
        self._engine = Engine.new_engine(info['default'], info, ship)

    def __getattr__(self, attr):
        """
        We reroute requests we don't have the answer for to our engine
        """
        if attr in self._info:
            return self._info[attr]

        if self._engine:
            return getattr(self._engine, attr)
        raise RuntimeError(f"Unknown engine property: {attr}")

    @property
    def engine(self):
        return self._engine


class Ship(_AbstractDrawObject):
    """
    A component that can float/fly in space, has health, can be destroyed,
    and other fun stuff!
    """

    #
    # How heavy is our ship? Heavier ships require more power in the engines
    # to go the same speed as smaller class ships
    # 
    WEIGHT_CLASS = {
        'A' : 1,
        'B' : 2,
        'C' : 3,
        'D' : 4,
    }

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

        self._hardpoints = [
            ShipHardpoint(x, self) for x in ship_info.get('hardpoints', [])
        ]

        self._engines = [
            ShipEngine(x, self) for x in ship_info.get('engines', [])
        ]

        self._data_location = ship_info['data_directory']

        # -- Internal Ship details
        self._thrust = Position()
        self._speed = Position()
        self._drag = Position(0.05, 0.05)
        self._change = Position()

        self._angle_delta = 0.0
        self._angle = 0.0

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

    @property
    def angle(self):
        return self._angle

    # -- More typical gameplay controls

    def fire_command(self, command):
        """
        Used to interact with hardpoints or other abilities.

        :param command: The action that we're taking
        :return: None
        """
        for sh in self._hardpoints:
            if not sh.hardpoint:
                continue

            if sh.command == command:
                sh.fire()

    @property
    def thrust(self):
        return self._thrust

    def set_thrust(self, thrust: Position):
        self._thrust = thrust

        if self._thrust.y > 0:
            emap(lambda x: x.engage(), self._engines)
        else:
            emap(lambda x: x.disengage(), self._engines)

    @property
    def angle_delta(self):
        return self._angle_delta
    
    def set_angle_delta(self, delta):
        self._angle_delta = delta

    def max_speed(self):
        """
        Calculate the max speed of this vessel based on the current
        engine power and it's class
        """
        total_power = functools.reduce(
            lambda x, y: x.power + y.power, self._engines
        ) if len(self._engines) > 1 else self._engines[0].power

        return total_power / Ship.WEIGHT_CLASS[self._class]

    # -- Overloaded update

    def update(self, delta_time):
        """
        The ship piloting logic goes in herew
        
        :note: We work in 2 dimentions with nealy everything here
        """
        self._speed.drag_calculation(self._drag)

        self._speed += self._thrust
        ms = self.max_speed()
        self._speed.clamp(-ms, ms)

        self._angle += self.angle_delta
        self._change.x = -math.sin(math.radians(self._angle)) * self._speed.y
        self._change.y = math.cos(math.radians(self._angle)) * self._speed.y

        self._change.x += -math.sin(math.radians(self._angle + 90)) * self._speed.x
        self._change.y += math.cos(math.radians(self._angle + 90)) * self._speed.x

        s = self.sprite()
        s.center_x += self._change.x
        s.center_y += self._change.y
        s.angle = int(self._angle)
        self.set_position(Position(s.center_x, s.center_y))

        super().update(delta_time)

        # Update all the components as well
        emap(lambda x: x.update(delta_time), self._hardpoints)
        emap(lambda x: x.update(delta_time), self._engines)

    # -- Base Class Requirements

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

        emap(lambda x: _must_contain(info, errors, *x), [
            ('display_name', str),
            ('class', str),
            ('description', str),
            ('mobile', bool),
            ('hull', int),
            ('shield', int),
            ('fuel', int),
            ('base_power', (int, float)),
        ])

        if not info['class'] in cls.WEIGHT_CLASS:
            errors.append(f"Weigth class: '{info['class']}' not known!")

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
