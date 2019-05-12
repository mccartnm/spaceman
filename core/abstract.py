
import arcade
from purepy import PureVirtualMeta, pure_virtual

from .utils import Position
from . import settings

class DrawEvent(object):
    """
    An object that we create from the window class that we pass down
    to the various objects.
    """
    def __init__(self, mouse: Position, window):

        self._mouse = mouse
        self._window = window

    @property
    def mouse(self):
        return self._mouse

    @property
    def window(self):
        return self._window


class TSprite(arcade.Sprite):
    """
    Base class for all sprites to work from.
    """
    BASE_STATE = 'life-static' # Required by all sprites

    def __init__(self, states, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._states = states
        self._state = BASE_STATE

    @property
    def state(self):
        return self._sprite_state

    def get_state_info(self):
        """
        Get the descriptor for this sprite/animation
        """
        return self._states[self._state]

    def set_sprite_state(self, state: str):
        """
        Set the sprite to an alternate state
        """
        if state in self._sprite_state:
            # Only if we have the state do we move into it.
            # No sense is failing hard
            self._sprite_state = state
        else:
            self._sprite_state = BASE_STATE

class _AbstractDrawObject(metaclass=PureVirtualMeta):
    """
    Any drawable object or structure should derive from this
    """
    SPRITE_BASED = 0
    PAINT_BASED  = 1

    def __init__(self):
        self._position = Position(0, 0)
        self._z_depth = 0

        # The sprite itself
        self._sprite = None

    @property
    def position(self) -> Position:
        return self._position

    @property
    def z_depth(self) -> int:
        return self._z_depth


    def set_position(self, position: Position):
        self._position = Position

    def set_x(self, x: int):
        self._position.x = x

    def set_y(self, y: int):
        self._position.y = y

    def set_z_depth(self, z: int):
        """
        Set the z position of this item to give the
        render engine an idea of when to draw it
        """
        self._z_depth = z

    def default_sprite(self) -> TSprite:
        """
        :return: TSprite
        """
        s = TSprite(scale=settings.get_setting('global_scale', 1.0))
        s.center_x = self.position.x
        s.center_y = self.position.y

    @pure_virtual
    def draw_method(self):
        """
        :return: The type of object this is (manual draw code or sprite based)
        """
        raise NotImplementedError()

    def load_sprite(self):
        """
        Overload to build and return the arcade.Sprite object
        that will be rendered at the various layers
        """
        raise NotImplementedError()

    def _retrieve_sprite_pvt(self):
        """
        Private call the render engine uses to load a sprite once
        """
        if self._sprite:
            return self._sprite
        else:
            self._sprite = self.load_sprite()
        return self._sprite

    def paint(self, draw_event: DrawEvent):
        """
        All classes have to overload this
        """
        raise NotImplementedError()
