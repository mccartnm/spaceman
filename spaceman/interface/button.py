
import arcade

from ..core.utils import Rect, Position, MouseEvent
from ..core.tobject import TSignal

from .iabstract import _AbstractInterfaceObject

class Button(_AbstractInterfaceObject):
    """
    Any kind of button that users can interact with
    """
    def __init__(self,
                 text: str = "",
                 geometry: Rect = Rect(),
                 parent = None):

        super().__init__(geometry, parent)
        self._text = text
        self._color = arcade.color.WHITE

    @property
    def color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def draw_method(self):
        """
        By default, all interface items are paint based
        """
        return _AbstractInterfaceObject.SHAPE_BASED |\
               _AbstractInterfaceObject.PAINT_BASED

    def paint(self, draw_event):
        """
        Paint the text
        """
        center = self.geometry.center()
        arcade.draw_text(
            text=self._text,
            start_x=center.x,
            start_y=center.y,
            color=self._color,
            align="center",
            anchor_x="center",
            anchor_y="center"
        )

    def shapes(self, draw_event):
        """
        Paint a basic beam
        """
        shapes = [self.background_shape()]
        return shapes

    @TSignal
    def clicked(self):
        """
        When we press the mouse down on this object, we click!
        Listeners, start you engines!
        """
        pass

    def on_mouse_press(self, mouse_event: MouseEvent) -> bool:
        """
        Called when we press the mouse down on this object
        :return: Boolean if we consume this thing
        """
        self.clicked()
        return True
