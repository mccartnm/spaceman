"""
Acbstract interfacing tools
"""

import arcade

from ..core.abstract import _AbstractDrawObject
from ..core.utils import Position, Rect, emap, MouseEvent
from ..core.tobject import TObject, TSignal

class _AbstractInterfaceObject(TObject, _AbstractDrawObject):
    """
    Anything that represents the users interface
    """
    def __init__(self, geometry: Rect = Rect(), parent = None):
        TObject.__init__(self)
        _AbstractDrawObject.__init__(self)

        self._geometry = geometry
        self._background_color = arcade.color.DIM_GRAY
        self._parent = parent

        if self._parent:
            self._parent.add_object(self)

    @property
    def geometry(self) -> Rect:
        if self._parent:
            return self._geometry.moved(self._parent.position)
        return self.local_geometry

    @property
    def local_geometry(self):
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
        By default, all interface items are shape based
        """
        return _AbstractDrawObject.SHAPE_BASED

    def on_mouse_press(self, mouse_event: MouseEvent) -> bool:
        """
        Called when we press the mouse down on this object
        :return: Boolean if we consume this thing
        """
        return True


class _TWidgetManager(TObject):
    """
    Singleton manager that holds onto all widgets and dolls out
    select input events to them.
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_known_widgets'):
            # Hash of widgets to their respective z-depth
            self._known_widgets = {}

        if not hasattr(self, '_window'):
            self._window = None

    @staticmethod
    def set_window(window):
        m = _TWidgetManager()
        m._window = window
        m._window.on_mouse_press.listen_post(m._on_mouse_press)

    @staticmethod
    def register_widget(widget):
        _TWidgetManager()._known_widgets.setdefault(widget.z_depth, []).append(widget)

    @staticmethod
    def deregister_widget(widget):
        layer = _TWidgetManager()._known_widgets.get(widget.z_depth, [])
        if widget in layer:
            layer.remove(widget)

    def _on_mouse_press(self, x, y, button, modifiers):
        """
        When the mouse is pressed, we walk through our widgets (top-down) and
        see if one of them consumes our click
        """
        event = MouseEvent(x, y, button, modifiers)
        for i in sorted(self._known_widgets.keys(), reverse=True):
            widgets = self._known_widgets[i]
            for w in widgets:
                if w.on_mouse_press(event):
                    return # Consumed!

class TWidget(TObject):
    """
    An object that can posses multiple draw objects
    for use later and simple "toggle" settings.
    """
    def __init__(self, position: Position = Position(), parent = None):
        super().__init__()

        # How we can move the entire widget if need be
        self._position = position

        self._objects = {
            'paint' : [],
            'sprite': [],
            'shapes': []
        }
        self._visible = False
        self._z_depth = 0
        self._dirty = False

        # Widget tree
        self._parent = parent
        self._children = []

        from ..core.render import RenderEngine
        if not self._parent:
            RenderEngine().add_widget(self)
        else:
            self._visible = self._parent._visible
            self._parent.add_child(self)

    @property
    def children(self) -> list:
        """
        Children widgets
        :return: list[TWidget]
        """
        return self._children

    @property
    def position(self) -> Position:
        if self._parent:
            return self._position + self._parent.position
        return self._position

    def size(self) -> Position:
        """
        Based on the total size occupied by our widget, return that size
        """
        rect = Rect(*self.position, 1, 1)
        for key in self._objects:
            for obj in self._objects[key]:
                rect = rect.united(obj.geometry)
        return rect

    def set_position(self, position: Position):
        """
        This this widget's position
        :param position: The new, global, position
        """
        self._position = position
        self.set_dirty(True)

    @property
    def dirty(self):
        return self._dirty
    
    def set_dirty(self, dirty):
        self._dirty = dirty

    @property
    def z_depth(self):
        return self._z_depth

    def set_z_depth(self, z_depth):
        _TWidgetManager.deregister_widget(self)
        self._z_depth = z_depth
        _TWidgetManager.register_widget(self)

    def add_object(self, obj: _AbstractInterfaceObject):
        """
        Add an object to our widget
        """
        if obj.draw_method() & _AbstractDrawObject.SPRITE_BASED:
            self._objects['sprite'].append(obj)

        if obj.draw_method() & _AbstractDrawObject.SHAPE_BASED:
            self._objects['shapes'].append(obj)

        if obj.draw_method() & _AbstractDrawObject.PAINT_BASED:
            self._objects['paint'].append(obj)

    def remove_object(self, obj: _AbstractInterfaceObject):
        """
        Remove an object from this widget
        """
        try:
            if obj.draw_method() & _AbstractDrawObject.SPRITE_BASED:
                self._objects['sprite'].remove(obj)

            if obj.draw_method() & _AbstractDrawObject.SHAPE_BASED:
                self._objects['shapes'].remove(obj)

            if obj.draw_method() & _AbstractDrawObject.PAINT_BASED:
                self._objects['paint'].remove(obj)

        except ValueError as e:
            pass

    def _set_parent(self, parent):
        """
        Set the parent of this widget. This is protected for now
        until we clean up the code and allow for dynamic child
        reallocation between widgets (children remove/addition)
        :param parent: TWidget
        :return: None
        """
        from ..core.render import RenderEngine
        RenderEngine().remove_widget(self)
        self._parent = parent

    def add_child(self, widget):
        """
        Add a relative child widget to this widget
        :param parent: TWidget
        :return: None
        """
        widget._set_parent(self)
        self._children.append(widget)

    def on_mouse_press(self, mouse_event: MouseEvent):
        """
        When we press the mouse down, we pass the event down to the
        drawable objects
        """
        for key in self._objects:
            for item in self._objects[key]:

                if not item.geometry.contains(Position(mouse_event.x, mouse_event.y)):
                    continue

                if item.on_mouse_press(mouse_event):
                    return True # Consumed!

        # If our own draw objects fail, let's try our chil widgets
        for w in self._children:
            if w.on_mouse_press(mouse_event):
                return True

        return False # Nothing was clicked

    def show(self):
        self._visible = True
        _TWidgetManager.register_widget(self)
        for c in self._children:
            c._visible = True
        self.set_dirty(True)

    def hide(self):
        self._visible = False
        _TWidgetManager.deregister_widget(self)
        for c in self._children:
            c._visible = False
        self.set_dirty(True) # Have to make sure it's cleared our

    def sprites(self, draw_event):
        """
        Get all sprites this widgets holds onto
        """
        sprites = []
        if self._visible:
            for item in self._objects['sprite']:
                d = item.sprite()
                if isinstance(d, (list, tuple)):
                    sprites.extend(d)
                else:
                    sprites.append(d)

        emap(lambda x: sprites.extend(x.sprites(draw_event)), self._children)

        return sprites

    def shapes(self, draw_event):
        """
        Obtain all shapes this widget holds on to so we may render in batch.
        :param draw_event: The DrawEvent object that we pass along
        :return: None
        """
        shapes = []
        if self._visible:
            for shape_item in self._objects['shapes']:
                shapes.extend(shape_item.shapes(draw_event))

        emap(lambda x: shapes.extend(x.shapes(draw_event)), self._children)

        return shapes

    def paint(self, draw_event):
        """
        Paint each of our items using their internal paint function
        """
        if not self._visible:
            return

        for item in self._objects['paint']:
            item.paint(draw_event)