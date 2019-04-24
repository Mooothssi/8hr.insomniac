import arcade
from inac8hr.wrappers.inac8hr_arcade import DrawCommands
from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.primitives import Point


class Container(Control):

    def __init__(self, position: Point):
        self.controls = []
        self.__position = position
        super().__init__(position)

    def draw(self):
        for c in self.controls:
            c.draw()

    def add_control(self, control: Control):
        self.controls.append(control)

    def get_position(self):
        return self.__position

    def set_position(self, value: Point):
        if len(self.controls) > 0:
            self.translate_controls(value.x, value.y)
        self.__position = value

    def translate_controls(self, x, y):
        dx, dy = x - self.position.x, y - self.position.y
        for c in self.controls:
            c.position.x += dx
            c.position.y += dy
    
    position = property(get_position, set_position)


class AnimatedContainer(Container):
    pass


class AnimatedTexturedMessageBox(AnimatedContainer):
    def __init__(self, position: Point, texture_filename: str,
                 width: int=500, height: int=500):
        super().__init__(position)
        self.texture = arcade.load_texture(texture_filename)
        self.width = width
        self.height = height
        self._alpha = 0
        self.alpha = 0

    def draw(self):
        DrawCommands.draw_textured_rectangle(self.position.x, self.position.y,
                                      self.width, self.height, self.texture, alpha=self.alpha)
        super().draw()

    def get_alpha(self):
        return self._alpha

    def set_alpha(self, value):
        if self.alpha < 254:
            if len(self.controls) > 0:
                for c in self.controls:
                    c.visible = False
        else:
            if len(self.controls) > 0:
                for c in self.controls:
                    c.visible = True
        self._alpha = value
    
    alpha = property(get_alpha, set_alpha)