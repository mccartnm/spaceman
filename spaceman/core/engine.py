"""
The engines of a ship
"""

import os
import yaml
import arcade

from .utils import _must_contain
from .abstract import _AbstractDrawObject, TSprite

class Engine(_AbstractDrawObject):
    """
    An engine - which is actually just the exhaust of the engine
    """
    WIDE = 'w' #< Takes two pixels for center
    THIN = 't' #< Takes one pixel for center

    # -- Known - Loaded engine descriptors
    _engine_prototypes = {}

    def __init__(self, info, ship):
        self._name   = info['name']
        self._power  = info['power']
        self._sprite = info['sprite']
        self._ship   = ship

    @classmethod
    def new_engine(cls, prototype: str, ship):
        return cls(cls._engine_prototypes[prototype], ship)

    def engage(self):
        """
        "turn on" the engine. This simply adds the sprite to the
        scene below the player.        
        """
        from .render import RenderEngine
        RenderEngine().add_object(self)

    def disengage(self):
        """
        "turn of" the engine.
        """
        from .render import RenderEngine
        RenderEngine().remove_object(self)

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

        for eg_info in info:
            if not isinstance(eg_info, dict):
                raise RuntimeError(
                    f"Each descriptor for {info_file} must be a dict"
                )

            map(lambda x: _must_contain(eg_info, errors, *x), [
                ('name', str),
                ('power', (int, float)),
                ('sprite', str)
            ])

            n = eg_info.get('name', info_file)
            if errors:
                print (f"ERROR ON: {n}:")
                print ("\n".join(errors))
                raise RuntimeError("Could not start game")

            if n in cls._engine_prototypes:
                raise RuntimeError(f"Duplicate engine name: {n}! Must be unique!")

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

        map(lambda x: _must_contain(info, errors, *x), [
            ('location', list),
            ('size', str),
            ('default', str),
        ])

        if errors:
            return

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
        We need to go load our sprite
        """
        scale = settings.get_setting('global_scale', 1.0)

        # For now, we'll just have life-static as a state. We may
        # want to think about this a bit more for the future
        states = {
            'life-static' : []
        }

        s = TSprite(states, scale=scale)
