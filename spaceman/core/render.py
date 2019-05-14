"""
Render tools and tech for the game
"""

import arcade

from .abstract import _AbstractDrawObject

class RenderEngine(object):
    """
    The main render toolkit (really it's just a wrapper around the
    arcade draw calls but let's us handle z depth and other such
    bits for our game)
    """

    # This is a singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        #
        # Because we're a singleton, we don't want to keep
        # overloading our attributes. This could probably
        # use a metaclass
        #
        if not hasattr(self, '_render_layers'):
            self._render_layers = {} # Sprite Based

    def add_object(self, obj: _AbstractDrawObject):
        """
        Add an object to either our sprite setup or our
        manual render process.
        """
        if obj.draw_method() == _AbstractDrawObject.SPRITE_BASED:
            #
            # This object is sprite based - we'll add it to our sprite
            # load for that depth. This way we can draw them in batches
            #
            sprite = obj._retrieve_sprite_pvt()
            self._render_layers.setdefault(
                obj.z_depth, [arcade.SpriteList(), []]
            )[0].append(sprite)

        else:
            #
            # This object uses the paint() function to paint out it's
            # environment.
            #
            self._render_layers.setdefault(
                obj.z_depth, [arcade.SpriteList(), []]
            )[1].append(obj)
        obj.set_in_scene(True)

    def unload_object(self, obj: _AbstractDrawObject):
        """
        Unload an object from our setup
        """
        if obj.z_depth in self._render_layers:
            if obj.draw_method() == _AbstractDrawObject.SPRITE_BASED:
                sprite = obj._retrieve_sprite_pvt()
                l = self._render_layers[obj.z_depth][0]
                l.remove(sprite)
            else:
                self._render_layers[obj.z_depth][1].remove(obj)
        obj.set_in_scene(False)

    def render(self, draw_event):
        """
        Main render loop
        """
        for i in sorted(self._render_layers.keys()):
            sprite_list, functional_draw = self._render_layers[i]

            # We draw functional items first
            for f in functional_draw:
                f.paint(draw_event)

            # The we draw the sprite list
            sprite_list.draw()
