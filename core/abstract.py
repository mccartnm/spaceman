
import os
import re
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
        self._state = None

        # Animation Controls
        self._frame = 0
        self._texture_index = 0
        self._texture_change_frames = settings.get_setting(
            'frames_between_change', 5
        )

        self.set_sprite_state(self.BASE_STATE)

    def set_frame_rate(self, frames):
        self._texture_change_frames = frames

    @property
    def state(self):
        return self._state

    def get_state_info(self):
        """
        Get the descriptor for this sprite/animation
        """
        return self._states[self._state]

    def current_state_is_animated(self):
        return isinstance(self.get_state_info(), list)

    def set_sprite_state(self, state: str):
        """
        Set the sprite to an alternate state
        """
        if self._state == state:
            return

        self._frame = 0
        if state in self._states:
            # Only if we have the state do we move into it.
            # No sense is failing hard
            self._state = state
        else:
            self._state = self.BASE_STATE

        # Make sure we set the initial texture
        info = self.get_state_info()
        if isinstance(info, list):
            self.texture = info[0] # Animated
        else:
            self.texture = info

    def update(self):
        """
        We update the TSprite based on the animation
        """
        super().update()

        state_info = self.get_state_info()
        if isinstance(state_info, list):
            # Animation!
            if self._frame % self._texture_change_frames == 0:
                self._texture_index += 1
                if self._texture_index >= len(state_info):
                    self._texture_index = 0
                self.texture = state_info[self._texture_index]
            self._frame += 1
        # else we have nothing to change

class _AbstractDrawObject(metaclass=PureVirtualMeta):
    """
    Any drawable object or structure should derive from this
    """
    SPRITE_BASED = 0
    PAINT_BASED  = 1

    ANIM_REGEX = re.compile(r"^(?P<name>.+)_(?P<frame>\d+)\.png$")

    def __init__(self):
        self._position = Position(0, 0)
        self._z_depth = 0

        # The sprite itself
        self._sprite = None

    @property
    def position(self):
        return self._position

    @property
    def z_depth(self) -> int:
        return self._z_depth

    def set_position(self, position: Position):
        self._position = position

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

    def build_states(self, texture_dir: str) -> dict:
        """
        Construct a state dictionary
        """
        scale = settings.get_setting('global_scale', 1.0)
        states = {}

        folders = filter(
            lambda x: os.path.isdir(
                os.path.join(texture_dir, x)
            ),
            os.listdir(texture_dir)
        )

        for folder in folders:

            this_dirname = os.path.join(texture_dir, folder)

            files = filter(
                lambda x: os.path.isfile(
                     os.path.join(this_dirname, x)
                ),
                os.listdir(this_dirname)
            )

            textures = filter(lambda x: x.endswith(".png"), files)

            animations = set()
            for texture in textures:

                anim_match = re.match(self.ANIM_REGEX, texture)
                is_anim = anim_match is not None

                name = texture[:-4] # Strip .png
                if anim_match:
                    d = anim_name.groupdict()
                    # Check if we've seen this animation before
                    name = d['name']
                    if name in animations:
                        continue
                    animations.add(name)

                loaded_texture = arcade.load_texture(
                    os.path.join(texture_dir, folder, texture),
                    scale=scale
                )

                state_name = f"{folder}-{name}"
                states.setdefault(state_name, [])
                if not is_anim:
                    states[state_name] = loaded_texture
                else:
                    states[state_name].append(loaded_texture)

        return states

    def default_sprite(self, texture_dir: str) -> TSprite:
        """
        :return: TSprite
        """
        scale = settings.get_setting('global_scale', 1.0)

        # -- Get the texture states
        states = self.build_states(texture_dir)

        s = TSprite(states, scale=scale)
        s.center_x = self.position.x
        s.center_y = self.position.y        
        return s

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
