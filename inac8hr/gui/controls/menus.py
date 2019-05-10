from ..basics import Point
from .base import AlignStyle
from .buttons import Button
from .labels import Tooltip
from i18n.loc import LocalizedText


class MenuButton(Button):

    def __init__(self, position: Point, texture_filename: str,
                 width: int=500, height: int=500):
        super().__init__(position, texture_filename, width, height)
        self.alignment |= AlignStyle.AlignXStyle.CENTER
    