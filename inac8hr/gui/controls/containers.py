import arcade
from inac8hr.wrappers.inac8hr_arcade import DrawCommands
from inac8hr.gui.controls.base import Control, AnimatedControl
from inac8hr.gui.basics import Point, RectangularRegion


class Container(Control):

    def __init__(self, position: Point, width: int=500, 
                 height: int=500, color: tuple=arcade.color.AMARANTH_PINK):
        self.children = []
        self.color = color
        super().__init__(position, width, height)

    def draw_children(self):
        for c in self.children:
            if c.visible:
                c.draw()

    def draw(self):
        arcade.draw_xywh_rectangle_filled(self.position.x, self.position.y,
                                          self.width, self.height, self.color)
        # self.region.draw()
        if len(self.children) > 0:
            self.draw_children()   

    def add_control(self, control: Control, relative: bool=False):
        self.children.append(control)
        self.add_event_handler_from_control(control)
        control.parent = self
        if relative:
            self.translate_relative()
        self.reset_region()

    def add_child(self, control: Control):
        self.add_control(control)

    def add_event_handler_from_control(self, control: Control):
        self.click_event += control.on_mouse_press

    def get_position(self):
        return super().get_position()

    def set_position(self, value: Point):
        if len(self.children) > 0:
            self.translate_controls(value.x, value.y)
        super().set_position(value)

    def translate_relative(self):
        offset = 0, 0
        if self.centeredly_drawn:
            offset = self.width // 2, self.height // 2
        for c in self.children:
            c.position.x += self.position.x - offset[0]
            c.position.y += self.position.y - offset[1]

    def translate_controls(self, x, y):
        dx, dy = x - self.position.x, y - self.position.y
        for c in self.children:
            c.position.x += dx
            c.position.y += dy

    position = property(get_position, set_position)


class AnimatedContainer(Container):
    pass


class AnimatedTexturedMessageBox(AnimatedContainer):
    def __init__(self, position: Point, texture_filename: str,
                 width: int=500, height: int=500):
        super().__init__(position, width, height)
        self.texture = arcade.load_texture(texture_filename)
        self._alpha = 0
        self.alpha = 0
        self.set_region_from_center()

    def draw(self):
        DrawCommands.draw_textured_rectangle(self.position.x, self.position.y,
                                      self.width, self.height, self.texture, alpha=self.alpha)
        super().draw_children()

    def get_alpha(self):
        return self._alpha

    def set_alpha(self, value):
        if self.alpha < 254:
            if len(self.children) > 0:
                for c in self.children:
                    c.visible = False
        else:
            if len(self.children) > 0:
                for c in self.children:
                    c.visible = True
        self._alpha = value
    
    alpha = property(get_alpha, set_alpha)