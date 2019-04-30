import arcade
from i18n.loc import LocalizedText
from inac8hr.wrappers.inac8hr_arcade import DrawCommands
from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.controls.containers import Container
from inac8hr.gui.basics import Point


class Button(Container):
    TEXTURE_LIMIT = 2
    STATE_NORMAL = 0
    PRESSED = 1
    HOVERED = 2

    def __init__(self, position: Point, texture_filename: str,
                 width: int=500, height: int=500):
        super().__init__(position, width, height) 
        self._textures = [arcade.load_texture(texture_filename)]
        self._current_tex_index = self.STATE_NORMAL
        self.alpha = 255
        self._background_drawn = False
        # self.set_region_from_center()

    def draw(self):
        DrawCommands.draw_textured_rectangle(self.position.x + (self.width//2), 
                                             self.position.y + (self.height//2),
                                             self.width, self.height, 
                                             self.current_texture)
        super().draw()

    def append_texture(self, file_name: str):
        self._textures.append(arcade.load_texture(file_name))
        assert(len(self._textures) <= self.TEXTURE_LIMIT)

    def change_texture(self, tex_no: int):
        assert(0 <= tex_no <= len(self._textures) - 1)
        self._current_tex_index = tex_no

    @property
    def current_texture(self):
        return self._textures[self._current_tex_index]

    def on_mouse_press(self, *args):
        super().on_mouse_press(*args)
        if self._mouse_down:
            self.change_texture(self.PRESSED)

    def on_mouse_release(self, *args):
        super().on_mouse_release(*args)
        self.change_texture(self.STATE_NORMAL)

