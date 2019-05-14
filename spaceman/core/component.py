"""
Component manger
"""

import os
import yaml
import arcade

from .hardpoint import Hardpoint
from .engine import Engine
from .player import Player
from .ship import Ship


class ComponentManager(object):
    """
    Spaceman is a game of items and objects for your ship, crew, and otherwise!

    To control the chaos, this manager will house most of the information required
    to provide these components in a simple, effective manner
    """

    def __init__(self, data_directory: str):
        """

        """
        self._data_path = data_directory

    @property
    def ships_data(self):
        return os.path.join(self._data_path, 'ships')

    @property
    def hardpoint_data(self):
        return os.path.join(self._data_path, 'components', 'hardpoints')

    @property
    def engine_data(self):
        return os.path.join(self._data_path, 'components', 'engines')

    def load(self):
        """
        Load any of the dynamic data we can!
        """
        # Hardpoints
        d = self.hardpoint_data
        for hardpoint_info_file in os.listdir(d):
            if not hardpoint_info_file.endswith('.si'):
                continue

            info_file = os.path.join(d, hardpoint_info_file)
            Hardpoint.add_info_file(info_file, d)

        # Engines
        d = self.engine_data
        for engine_info_file in os.listdir(d):
            if not engine_info_file.endswith('.si'):
                continue

            info_file = os.path.join(d, engine_info_file)
            Engine.add_info_file(info_file, d)

        # Ships
        d = self.ships_data
        for ship_dir in os.listdir(d):
            data_dir = os.path.join(d, ship_dir)
            info_file = os.path.join(data_dir, 'info.si')
            if not os.path.isfile(info_file):
                continue

            Ship.add_prototype(ship_dir, info_file)
