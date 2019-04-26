import arcade
import pyglet
from i18n.loc import LocalizedText
from inac8hr.wrappers.inac8hr_arcade import DrawCommands
from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.basics import Point


class Button(Control):
    def __init__(self, position: Point, texture_filename: str,
                 width: int=500, height: int=500):
        super().__init__(position, width, height)
        self.texture = arcade.load_texture(texture_filename)
        self.alpha = 255
        self.set_region_from_center()

    def draw(self):
        DrawCommands.draw_textured_rectangle(self.position.x, self.position.y,
                                             self.width, self.height, self.texture, alpha=self.alpha)
