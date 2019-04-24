import arcade
from i18n.loc import LocalizedText
from inac8hr.wrappers.inac8hr_arcade import DrawCommands
from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.primitives import Point


class Label(Control):
    def __init__(self, position: Point=Point(0, 0), text: str="",
                 size: int=12, color: tuple=arcade.color.BLACK, align="left", font_name=('calibri','arial')):
        super().__init__(position)
        self.text = text
        self.fore_color = color
        self.align = align
        self.font_name = font_name
        self.__font_size__ = size

    @property
    def font_size(self):
        return self.__font_size__

    def draw(self):
        if self.text != "" and self.visible:
            arcade.draw_text(str(self.text), self.position.x, self.position.y,
                             self.fore_color, self.font_size, font_name=self.font_name, align=self.align)


class LocalizedLabel(Label):
    def __init__(self, position: Point, key: str="LocalizedText/None",
                 size: int=12):
        super().__init__(position, key, size)
        self.loc_text = LocalizedText(key)

    def get_text(self):
        return str(self.loc_text)

    def set_text(self, value):
        self._text = value

    text = property(get_text, set_text)