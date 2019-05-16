"""
Acbstract interfacing tools
"""

import arcade

from ..core.abstract import _AbstractDrawObject
from ..core.utils import Position, Rect, emap

class _AbstractInterfaceObject(_AbstractDrawObject):
    """
    Anything that represents the users interface
    """
    def __init__(self, geometry: Rect = Rect(), parent = None):
        super().__init__()
        self._geometry = geometry
        self._background_color = arcade.color.DARK_GRAY
        self._parent = parent

        if self._parent:
            self._parent.add_object(self)

    @property
    def geometry(self) -> Rect:
        return self._geometry

    @property
    def background_color(self):
        """
        The background of our object (if we choose to paint it)
        :return: arcade.color
        """
        return self._background_color

    def set_parent(self, parent):
        self._parent = parent

    def set_dirty(self, dirty: bool):
        self._parent.set_dirty(dirty)

    def background_shape(self):
        """
        Have arcade paint our rect
        """
        return arcade.create_rectangle(
            *(self.geometry.to_arcade_rect()),
            self._background_color
        )
    
    def set_background_color(self, color):
        """
        :param color: arcade.color
        """
        self._background_color = color
    
    def set_geometry(self, geometry: Rect):
        """
        Set the geometry of our object
        """
        self._geometry = geometry

    def draw_method(self):
        """
        By default, all interface items are paint based
        """
        return _AbstractDrawObject.SHAPE_BASED


class TWidget(object):
    """
    An object that can posses multiple draw objects
    for use later and simple "toggle" settings.
    """
    def __init__(self):
        self._objects = {
            'paint' : [],
            'sprite': arcade.SpriteList(),
            'shapes': []
        }
        self._visible = False
        self._z_depth = 0
        self._dirty = False

        from ..core.render import RenderEngine
        RenderEngine().add_widget(self)

    @property
    def dirty(self):
        return self._dirty
    
    def set_dirty(self, dirty):
        self._dirty = dirty

    @property
    def z_depth(self):
        return self._z_depth

    def set_z_depth(self, z_depth):
        self._z_depth = z_depth

    def add_object(self, obj: _AbstractInterfaceObject):
        """
        Add an object to our widget
        """
        if obj.draw_method() == _AbstractDrawObject.SPRITE_BASED:
            self._objects['sprite'].append(obj) # WRONG - FIXME LATER
        elif obj.draw_method() == _AbstractDrawObject.SHAPE_BASED:
            self._objects['shapes'].append(obj)
        else:
            self._objects['paint'].append(obj)

    def remove_object(self, obj: _AbstractInterfaceObject):
        """
        Remove an object from this widget
        """
        try:
            if obj.draw_method() == _AbstractDrawObject.SPRITE_BASED:
                self._objects['sprite'].remove(obj)
            elif obj.draw_method() == _AbstractDrawObject.SHAPE_BASED:
                self._objects['shapes'].remove(obj)
            else:
                self._objects['paint'].remove(obj)
        except ValueError as e:
            pass

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False

    def shapes(self, draw_event):
        """
        Render all the items this widget holds on to.
        :param draw_event: The DrawEvent object that we pass along
        :return: None
        """
        if not self._visible:
            return

        shapes = []
        for shape_item in self._objects['shapes']:
            shapes.extend(shape_item.shapes(draw_event))

        return shapes
