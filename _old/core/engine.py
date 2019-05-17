"""
The engines of a ship
"""

import re
import os
import yaml
import arcade
import math

import numpy

from . import settings
from .utils import _must_contain, Position, emap
from .abstract import _AbstractDrawObject, TSprite

class Engine(_AbstractDrawObject):
    """
    An engine - which is actually just the exhaust of the engine
    """
    WIDE = 'w' #< Takes two pixels for center
    THIN = 't' #< Takes one pixel for center

    CARDINALS = ('n', 's', 'e', 'w')

    # -- Known - Loaded engine descriptors
    _engine_prototypes = {}

    def __init__(self, engine_info, ship_engine_info, ship):
        super().__init__()
        self._name        = engine_info['name']
        self._power       = engine_info['power']
        self._sprite_path = engine_info['sprite']
        self._ship_ei = ship_engine_info
        self._ship    = ship

        self.set_z_depth(-1) # To render under ship

        self._on = False

    @classmethod
    def new_engine(cls, prototype: str, info: dict, ship = None):
        return cls(cls._engine_prototypes[prototype], info, ship)

    @property
    def power(self):
        return self._power

    def engage(self):
        """
        "turn on" the engine. This simply adds the sprite to the
        scene below the player.        
        """
        if self._on:
            return

        self._on = True
        from .render import RenderEngine
        RenderEngine().add_object(self)

    def disengage(self):
        """
        "turn of" the engine.
        """
        if not self._on:
            return

        self._on = False
        from .render import RenderEngine
        RenderEngine().unload_object(self)

    @classmethod
    def add_info_file(cls, info_file: str, data_directory: str):
        """
        Pick apart an engine .si file to understand our verify prototypes
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

        from .ship import Ship
        for eg_info in info:
            if not isinstance(eg_info, dict):
                raise RuntimeError(
                    f"Each descriptor for {info_file} must be a dict"
                )

            emap(lambda x: _must_contain(eg_info, errors, *x), [
                ('name', str),
                ('power', (int, float)),
                ('sprite', str),
                ('minimum_class', str)
            ])

            n = eg_info.get('name', info_file)
            if errors:
                print (f"ERROR ON: {n}:")
                print ("\n".join(errors))
                raise RuntimeError("Could not start game")

            if eg_info['minimum_class'] not in Ship.WEIGHT_CLASS:
                raise RuntimeError(
                    f"Unkown engine minimum_class: '{eg_info['minimum_class']}'"
                )

            if n in cls._engine_prototypes:
                raise RuntimeError(f"Duplicate engine name: {n}! Must be unique!")

            eg_info['sprite'] = os.path.join(data_directory, eg_info['sprite'])
            if not os.path.exists(eg_info['sprite']):
                raise RuntimeError(f"Sprite(s): {eg_info['sprite']} does not exist!")

            cls._engine_prototypes[n] = eg_info

    @classmethod
    def verify_ship_engine(cls, info, errors):
        """
        Verify that this engine information is enough to
        draw the dhip properly
        """
        if not isinstance(info, dict):
            errors.append("Engine should be a dictionary!")
            return

        emap(lambda x: _must_contain(info, errors, *x), [
            ('location', list),
            ('size', str),
            ('default', str),
            ('direction', str),
        ])

        if errors:
            return

        if info['direction'] not in cls.CARDINALS:
            errors.append(
                f"direction must be one of: {', '.join(cls.CARDINALS)}"
            )

        if info['size'] not in (cls.WIDE, cls.THIN):
            errors.append(
                f"Engine size must be one of: '{cls.WIDE}', '{cls.THIN}'"
            )

        location = info['location']
        if len(location) != 2:
            errors.append("'location' requires [x, y] coordinates")
        elif any((isinstance(x, int) == False for x in location)):
            errors.append("'location' components should be integers")

    def draw_method(self):
        return _AbstractDrawObject.SPRITE_BASED

    def load_sprite(self):
        """
        Load our sprite and put it wherever it's supposed to be
        """
        s = self.load_basic(*os.path.split(self._sprite_path))
        s.center_x = self.position.x
        s.center_y = self.position.y
        return s

    def update(self, draw_event):
        """
        Overload to handle keeping up with the ship
        """

        if not self._ship:
            return # Nothing to draw yet

        if not self._on:
            return # Not ine the scene - nothing to render

        scale = settings.get_setting('global_scale', 1.0)

        #
        # Find the relative location of the engine based on the
        # active location and angle
        #
        ship_sprite = self._ship.sprite()
        s = self.sprite()

        # This should always be the same
        s.angle = int(self._ship.angle)

        # FIXME: This could be cached 
        this_location = Position(self._ship_ei['location']) * scale
        ship_center = Position(
            ship_sprite.width / 2,
            ship_sprite.height / 2,
        )

        this_sprite_center = Position(
            s.height / 2,
            s.height / 2
        )
        relative_location = this_location - ship_center
        # -- End FIXME

        rads = math.radians(self._ship.angle)

        mat = numpy.array([
            [math.cos(rads), -math.sin(rads), self._ship.position.x],
            [math.sin(rads), math.cos(rads),  self._ship.position.y],
            [0,              0,               1]
        ])

        if self._ship_ei['direction'] == 's':
            relative_location.y += this_sprite_center.y

            if self._ship_ei['size'] == 'w':
                relative_location.x += 1

        a = numpy.matmul(mat, [relative_location.x, -relative_location.y, 1])
        self.set_position(Position(a[0], a[1]))

        s.center_x = int(self.position.x)
        s.center_y = int(self.position.y)

        super().update(draw_event)
