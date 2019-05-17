
import os
import arcade

import pyglet.gl as gl

from .hardpoint import Hardpoint
from .engine import Engine
from .player import Player
from .ship import Ship

from .tobject import TObject, TSignal
from .abstract import DrawEvent
from .utils import Position, FPSCounter
from .render import RenderEngine
from .campaign import CampaignLoader, Campaign
from .component import ComponentManager

from ..interface.user import UserInterface
from ..interface.iabstract import _TWidgetManager

DEV_MODE = True
ONCE_FLAG = False

class Spaceman(TObject, arcade.Window):
    """
    The main window y'all!
    """
    def __init__(self, w, h, title):
        TObject.__init__(self)
        arcade.Window.__init__(self, w, h, title)

        #
        # Widget manager started first to assert other widgets
        # will be created properly
        #
        _TWidgetManager.set_window(self)

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

        # Get the render engine
        self._render_engine = RenderEngine()
        self._render_engine.set_data_directory(self._data_path)

        self._component_manager = ComponentManager(self._data_path)

        # Initial information
        self._mouse_position = Position(0, 0)
        self._mouse_delta = Position(0, 0)

        # The campaign loading and selection
        self._camp_loader = CampaignLoader()
        self._campaign = None # We load this later

        # The players active ship
        self._player = Player()

        # The interface for the user's current health and otherwise
        self._interface = UserInterface(self._player)

        if DEV_MODE:
            self._fps = FPSCounter()

    @property
    def data_path(self):
        return self._data_path

    def setup(self):
        """
        We setup the game!
        """
        arcade.set_background_color(arcade.color.BLACK)
        # arcade.draw_text("Loading...", 10, 10, arcade.color.WHITE, 12)

        # Step 1!
        self._component_manager.load()

        if DEV_MODE:
            self._campaign = self._camp_loader.dev_campaign()
            self._campaign.basic_start(self._player, self)

        self._interface.show()

    # -- Overloaded interface

    def on_key_press(self, key, modifiers):
        """
        When we press a key
        """
        if self._player.on_key_press(key, modifiers):
            return

    def on_key_release(self, key, modifiers):
        """
        When we press a key
        """
        if self._player.on_key_release(key, modifiers):
            return

    @TSignal
    def on_mouse_motion(self, x, y, dx, dy):
        """
        When the user moves their mouse, what sould we do?
        """
        self._mouse_position = Position(x, y)
        self._mouse_delta = Position(dx, dy)

    @TSignal
    def on_mouse_press(self, x, y, button, modifiers):
        """
        When the user presses the mouse down, we attempt to feed that information
        to our various listeners
        """
        pass # TSignal will do the heavy lifting

    @TSignal
    def on_mouse_release(self, x, y, button, modifiers):
        """
        When the user releases the mouse, we attempt to feed that information
        to our various listeners
        """
        pass # TSignal will do the heavy lifting

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

        if DEV_MODE:
            fps = self._fps.get_fps()
            arcade.draw_text(f"FPS: {fps:3.0f}", 10, 10, arcade.color.WHITE, 12)
            self._fps.tick()

    def update(self, delta_time):
        """
        Update our scene!
        """
        # -- For the moment -- Might be able to improve the logic of this
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        self._player.update(delta_time)
