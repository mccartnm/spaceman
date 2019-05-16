
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

    This class uses the "state" structure to allow for dynamic loading
    of states when required.

    TODO: Add more documentation
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

    def set_position(self, position: Position):
        self.center_x = position.x
        self.center_y = position.y

    @property
    def state(self):
        return self._state

    def get_state_info(self):
        """
        Get the descriptor for this sprite/animation
        """
        return self._states[self._state]

    def current_state_is_animated(self):
        """
        :return: There are multiple textures to this sprite
        """
        si = self.get_state_info()
        return isinstance(si, list) and len(si) > 1

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
        if isinstance(state_info, list) and len(state_info) > 1:
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

    # Bitwise flags to allow for sprite _and_ paint-based objects
    SPRITE_BASED = 0x00000001
    PAINT_BASED  = 0x00000010
    SHAPE_BASED  = 0x00000100

    ANIM_REGEX = re.compile(r"^(?P<name>.+)_(?P<frame>\d+)\.png$")

    def __init__(self):
        self._position = Position(0, 0)
        self._velocity = Position(0, 0)
        self._z_depth = 0

        # The sprite itself
        self._sprite = None
        self._is_in_scene = False

    @property
    def position(self):
        return self._position

    @property
    def z_depth(self) -> int:
        return self._z_depth

    @property
    def is_in_scene(self):
        return self._is_in_scene

    def sprite(self):
        return self._retrieve_sprite_pvt()

    def add_to_scene(self):
        """
        This this object to our scene at the given depth
        :return: None
        """
        from .render import RenderEngine
        RenderEngine().add_object(self)

    def remove_from_scene(self):
        from .render import RenderEngine
        RenderEngine().unload_object(self)

    def set_in_scene(self, in_scene: bool):
        """
        Set when adding this to the render engine for rendering.

        Unset when we're done with it
        :param in_scene: Boolean if we're in the scene
        :return: None
        """
        self._is_in_scene = in_scene

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
        if self.is_in_scene:
            raise RuntimeError("Attempting to change the z-depth while"
                               " in scene. This is not yet supported")
        self._z_depth = z

    def set_velocity(self, velocty: Position):
        """
        Set the speed at which this object is traveling (if any)
        """
        self._velocity = velocty
        if self.draw_method() == _AbstractDrawObject.SPRITE_BASED:
            self.sprite().change_x = velocty.x
            self.sprite().change_y = velocty.y

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

    def load_basic(self, texture_dir: str, name: str) -> list:
        """
        :param texture_dir: Root location for the texture
        :param name: The name of this texture
        :return: list[arcade.Texture]|arcade.Texture
        """
        scale = settings.get_setting('global_scale', 1.0)
        textures = []

        basic = os.path.join(texture_dir, name)
        if os.path.isfile(basic + '.png'):
            textures.append(arcade.load_texture(
                basic + '.png', scale=scale
            ))
        elif os.path.isdir(basic):
            for filename in sorted(os.listdir(basic)):
                if re.match(r'^' + name + r'_[\d]+\.png$', filename):
                    textures.append(arcade.load_texture(
                        os.path.join(basic, filename),
                        scale=scale
                    ))

        states = {
            'life-static' : textures
        }

        s = TSprite(states, scale=scale)
        return s

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

    def shapes(self, draw_event: DrawEvent):
        """
        A function that returns arcade.shapes to enable bulk render calls
        for hand-made components
        """
        raise NotImplementedError()

    def update(self, delta_time):
        """
        Update this object. If the object is not a sprite, then this
        does nothing by default.
        :param delta_time: float of time passed sincle the last update
        :return: None
        """
        if self.draw_method() == _AbstractDrawObject.SPRITE_BASED:
            self.sprite().update()
