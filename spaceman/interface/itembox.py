"""
Item box sprite object
"""

import os
import arcade

from ..core.settings import get_setting
from ..core.utils import Rect, Position

from .iabstract import _AbstractInterfaceObject

class ItemBox(_AbstractInterfaceObject):
    """
    Box that can contain an item 
    """
    def __init__(self, parent = None):

        geo = Rect(0, 0, 32, 32) # Linked to image size
        super().__init__(geo, parent=parent)

        self._box = None

        self._item = None
        self._item_sprite = None

    def draw_method(self):
        """
        The item box is comprized of sprites only
        """
        return _AbstractInterfaceObject.SPRITE_BASED

    def sprite(self):
        """
        The sprites that we're using for this item box
        :return: list[TSprite]
        """
        if self._box is None:
            scale = get_setting('global_scale', 1.0)

            self._box = self.load_basic(
                texture_dir=os.path.join(
                    self.data_directory(), 'objects', 'interface'
                ),
                name='item_box',
                scale=scale * 1.5
            )
            self._box.set_position(self.geometry.center())

        if self._item:
            # TODO
            pass

        return [self._box]
