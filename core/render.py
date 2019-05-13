"""
Render tools and tech for the game
"""

import arcade

from .abstract import _AbstractDrawObject

class RenderEngine(object):
    """
    The main render toolkit
    """

    # This is a singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._render_layers = {} # Sprite Based

    def add_object(self, obj: _AbstractDrawObject):
        """
        Add an object to either our sprite setup or our
        manual render process.
        """
        if obj.draw_method() == _AbstractDrawObject.SPRITE_BASED:
            self._render_layers.setdefault(
                obj.z_depth, [arcade.SpriteList(), []]
            )[0].append(obj._retrieve_sprite_pvt())
        else:
            self._render_layers.setdefault(
                obj.z_depth, [arcade.SpriteList(), []]
            )[1].append(obj)

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

    def render(self, draw_event):
        """
        Main render loop
        """
        for i in sorted(self._render_layers.keys()):
            sprite_list, functional_draw = self._render_layers[i]

            # We draw functional items first
            map(lambda x: x.paint(draw_event), functional_draw)

            # The we draw the sprite list
            sprite_list.draw()
