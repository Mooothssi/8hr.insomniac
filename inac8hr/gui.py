import arcade
from i18n.loc import LocalizedText
from inac8hr.wrappers.inac8hr_arcade import DrawCommands


class Point():
    """
        A Cartesian point in a window
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, another):
        return Point(self.x + another.x, self.y + another.y)

    def __sub__(self, another):
        return Point(self.x - another.x, self.y - another.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Control():
    def __init__(self, position: Point):
        self.position = position
        self.visible = True

    def on_draw(self):
        if self.visible:
            self.draw()

    def draw(self):
        pass

    def clocked_update(self):
        pass

    def show(self):
        self.visible = True
        self.on_shown()

    def on_shown(self):
        pass

class AnimatedControl(Control):
    pass


class Label(Control):
    def __init__(self, position: Point=Point(0, 0), text: str="",
                 size: int=12, color: tuple=arcade.color.BLACK):
        super().__init__(position)
        self.text = text
        self.fore_color = color
        self.__font_size__ = size

    @property
    def font_size(self):
        return self.__font_size__

    def draw(self):
        if self.text != "":
            arcade.draw_text(str(self.text), self.position.x, self.position.y,
                             self.fore_color, self.font_size)


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


class AnimatedTexturedMessageBox(AnimatedControl):
    def __init__(self, position: Point, texture_filename: str,
                 width: int=12):
        super().__init__(position)
        self.texture = arcade.load_texture(texture_filename)
        self.width = 500
        self.height = 500
        self.alpha = 0

    def draw(self):
        DrawCommands.draw_textured_rectangle(self.position.x, self.position.y,
                                      self.width, self.height, self.texture, alpha=self.alpha)

class ScrollablePaneView(Control):

    def __init__(self):
        self.__items__ = []

    @property
    def items(self):
        return self.__items__
