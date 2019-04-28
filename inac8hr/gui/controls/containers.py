import arcade
from inac8hr.wrappers.inac8hr_arcade import DrawCommands
from inac8hr.gui.controls import AlignStyle, Control, AnimatedControl
from inac8hr.gui.basics import Point, RectangularRegion
from inac8hr.imports import ExtendedSpriteList


class Container(Control):

    def __init__(self, position: Point, width: int=500, 
                 height: int=500, color: tuple=arcade.color.AMARANTH_PINK):
        self.children = []
        self.color = color
        self._child_spr_list = ExtendedSpriteList()
        super().__init__(position, width, height)

    def draw_children(self):
        for c in self.children:
            if c.visible:
                c.draw()

    def draw(self):
        arcade.draw_xywh_rectangle_filled(self.position.x, self.position.y,
                                          self.width, self.height, self.color)
        if len(self.children) > 0:
            self.draw_children()

    def add_control(self, control: Control, relative: bool=False):
        self.children.append(control)
        self.add_event_handler_from_control(control)
        if relative:
            self.translate_relative(control)
        control.parent = self
        control._apply_behaviour()
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

    def translate_relative(self, control):
        offset = 0, 0
        if self.centeredly_drawn:
            offset = self.width // 2, self.height // 2
        control.position.x += self.position.x - offset[0]
        control.position.y += self.position.y - offset[1]
        # for c in self.children:
        #     c.position.x += self.position.x - offset[0]
        #     c.position.y += self.position.y - offset[1]

    def translate_controls(self, x, y):
        dx, dy = x - self.position.x, y - self.position.y
        for c in self.children:
            c.position.x += dx
            c.position.y += dy

    def on_window_resize(self, *args):
        width, height = args
        self.width = width
        self.height = height
        for c in self.children:
            if c.alignment & AlignStyle.AlignXStyle.CENTER:
                c.align_center()
            else:
                c._align_to_anchors()

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
        self.anchors |= self.ANCHOR_RIGHT | self.ANCHOR_TOP
        self.set_region_from_center()

    def draw(self):
        DrawCommands.draw_textured_rectangle(self.position.x + (self.width//2), self.position.y + (self.height//2),
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