import arcade
import pyglet
from i18n.loc import LocalizedText
from inac8hr.wrappers.inac8hr_arcade import DrawCommands
from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.basics import Point
from inac8hr.gui.controls.styles import AlignStyle


class Label(Control):

    def __init__(self, position: Point=Point(0, 0), text: str="",
                 size: int=12, color: tuple=arcade.color.BLACK, align: AlignStyle=AlignStyle.NONE, font_name=('calibri','arial')):
        super().__init__(position)
        self.__label__ = pyglet.text.Label(text, font_size=size, x=position.x,
                                           y=position.y)
        self.alignment = align
        self.text = text
        self.fore_color = color
        self.font_name = font_name
        self.__font_size__ = size
        

    @property
    def font_size(self):
        return self.__font_size__

    # def set_text(self, value):
    #     self.__label__.text = value

    # def get_text(self):
    #     return self.__label__.text

    # text = property(get_text, set_text)

    def draw(self):
        if self.text != "" and self.visible:
            arcade.draw_text(str(self.text), self.position.x, self.position.y,
                             self.fore_color, self.font_size, font_name=self.font_name,
                             align=self._get_text_alignment(), width=self.width, anchor_x=self._get_anchors_x(),
                             anchor_y=self._get_anchors_y())

    def _get_text_alignment(self):
        if self.alignment & AlignStyle.AlignXStyle.CENTER:
            return "center"
        elif self.alignment & AlignStyle.AlignXStyle.RIGHT:
            return "right"
        else:
            return "left"

    def _get_anchors_x(self):
        if self.anchors & self.ANCHOR_RIGHT:
            return "right"
        else:
            return "left"

    def _get_anchors_y(self):
        if self.alignment & AlignStyle.AlignYStyle.TOP:
            return "top"
        else:
            return "bottom"


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