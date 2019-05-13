
import os
import arcade

from .hardpoint import Hardpoint
from .player import Player
from .ship import Ship
from .abstract import DrawEvent
from .utils import Position
from .render import RenderEngine
from .campaign import CampaignLoader, Campaign

DEV_MODE = True

class Spaceman(arcade.Window):
    """
    The main window y'all!
    """
    def __init__(self, w, h, title):
        super().__init__(w, h, title)

        #
        # Boot happens in a few steps
        # 1. We establish all the dynamic objects that can be loaded.
        #    - This includes: items, ships, hardpoints
        # 2. Once we've loaded all the things, we create our player and
        #    set up the initial world.
        # 3. Only then do we give the user control.
        #

        # Where we store all of the dynamic game data
        self._data_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))
                )
            ),
            'data'
        )

        # Initial information
        self._mouse_position = Position(0, 0)
        self._mouse_delta = Position(0, 0)

        # The campaign loading and selection
        self._camp_loader = CampaignLoader()
        self._campaign = None # We load this later

        # The players active ship
        self._player = Player()

        # Step 1!
        self.load_data()

        # Get the render engine
        self._render_engine = RenderEngine()

    @property
    def ships_data(self):
        return os.path.join(self._data_path, 'ships')

    @property
    def hardpoint_data(self):
        return os.path.join(self._data_path, 'hardpoints')

    def setup(self):
        """
        """
        arcade.set_background_color(arcade.color.BLACK)

        if DEV_MODE:
            self._campaign = self._camp_loader.dev_campaign()
            self._campaign.basic_start(self._player, self)

    # -- Overloaded interface
    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_position = Position(x, y)
        self._mouse_delta = Position(dx, dy)

    def on_draw(self):
        """
        Render the scene
        """
        arcade.start_render()

        #
        # We oush all of the render logic to our engine
        #
        event = DrawEvent(self._mouse_position, self)
        self._render_engine.render(event)

    def load_data(self):
        """
        Load any of the dynamic data we can!
        """
        # Hardpoints
        d = self.hardpoint_data
        for hardpoint_info_file in os.listdir(d):
            info_file = os.path.join(d, hardpoint_info_file)
            Hardpoint.add_info_file(info_file, d)

        # Ships
        d = self.ships_data
        for ship_dir in os.listdir(d):
            data_dir = os.path.join(d, ship_dir)
            info_file = os.path.join(data_dir, 'info.si')
            if not os.path.isfile(info_file):
                continue
            Ship.add_prototype(ship_dir, info_file)
