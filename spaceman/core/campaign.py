"""
Campaign tools
"""

import yaml
import arcade

from .ship import Ship
from .utils import Position
from .player import Player

from .render import RenderEngine

class Map(object):
    """
    A single map within a campaign
    """
    def __init__(self):
        pass # TODO

class Campaign(object):
    """
    A campaign holds all of the story information required
    to play through our tails of adventure!
    """
    def __init__(self):
        pass # TODO

    def basic_start(self, player: Player, window):
        """
        When using the dev mode, we often just want to jump into a
        map or environment to work on mechanics and other game elements
        :param player: Our current Player
        :return: None
        """
        player.set_ship(
            Ship.new_ship("Skalk", position=Position(250, 230))
        )
        player.ship.add_to_scene()

        from ..draw.starfield import Starfield
        self._background = Starfield(window)
        RenderEngine().add_object(self._background)

class CampaignLoader(object):
    """
    Yaml parser for reading and understanding a campaign
    """
    def __init__(self):
        self._found_campaigns = {}

    def dev_campaign(self):
        """
        :return: A default Campaign for testing
        """
        return Campaign()
