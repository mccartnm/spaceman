"""
Render tools and tech for the game
"""

import arcade

from .abstract import _AbstractDrawObject
from .utils import emap

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

        if not hasattr(self, '_widget_layers'):
            self._widget_layers = {}

        if not hasattr(self, '_cached_shapes'):
            self._cached_shapes = {}

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
                obj.z_depth, [arcade.SpriteList(), [], []]
            )[0].append(sprite)

        elif obj.draw_method() == _AbstractDrawObject.SHAPE_BASED:
            #
            # We have a function to return a list of shapes for use to draw
            #
            self._render_layers.setdefault(
                obj.z_depth, [arcade.SpriteList(), [], []]
            )[2].append(obj)

        else:
            #
            # This object uses the paint() function to paint out it's
            # environment.
            #
            self._render_layers.setdefault(
                obj.z_depth, [arcade.SpriteList(), [], []]
            )[1].append(obj)
        obj.set_in_scene(True)

    def unload_object(self, obj: _AbstractDrawObject):
        """
        Unload an object from our setup
        """
        if obj.z_depth in self._render_layers:
            if obj.draw_method() == _AbstractDrawObject.SPRITE_BASED:
                self._render_layers[obj.z_depth][0].remove(
                    obj._retrieve_sprite_pvt()
                )
            elif obj.draw_method() == _AbstractDrawObject.SHAPE_BASED:
                self._render_layers[obj.z_depth][2].remove(obj)
            else:
                self._render_layers[obj.z_depth][1].remove(obj)
        obj.set_in_scene(False)


    def add_widget(self, widget):
        """
        Add a widget to the game. This is 
        """
        self._widget_layers.setdefault(widget.z_depth, []).append(widget)

    def render(self, draw_event):
        """
        Main render loop
        """

        #
        # Render the game objects - Trying to render bulk where
        # possible.
        #
        for i in sorted(self._render_layers.keys()):
            sprite_list, functional_draw, shape_based = self._render_layers[i]

            # We draw functional items first
            for f in functional_draw:
                f.paint(draw_event)

            # The we draw the sprite list
            sprite_list.draw()

            # We'll do our shapes last - in one punch
            # shapes = arcade.ShapeElementList()
            # for sb in shape_based:
                # emap(lambda x: shapes.append, sb.shapes(draw_event))
            # shapes.draw()

        #
        # The interface and other widgets render on top. This might
        # change one day but for now - we'll just ride with this
        #

        for i in sorted(self._widget_layers.keys()):
            widgets = self._widget_layers[i]

            whash = tuple(widgets)
            if whash in self._cached_shapes:

                shapes = self._cached_shapes[whash]
                if any(w.dirty for w in widgets):
                    # We need a new ShapeElementList
                    for s in shapes[:]:
                        shapes.remove(s)

                    for widget in widgets:
                        emap(lambda x: shapes.append, widget.shapes(draw_event))
                        widget.set_dirty(False)
            else:
                shapes = self._cached_shapes.setdefault(
                    whash, arcade.ShapeElementList()
                )

                for widget in widgets:
                    emap(shapes.append, widget.shapes(draw_event))
                    widget.set_dirty(False)

            shapes.draw()
